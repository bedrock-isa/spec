`timescale 1ns/1ps
`default_nettype none

// Generated from build/generated/allocation_plan.json.
// Do not edit by hand.

package bedrock_decode_pkg;
  import bedrock_pkg::*;

  localparam int BEDROCK_DECODE_OPCODE_COUNT = 211;
  localparam int BEDROCK_DECODE_OPCODE_ID_BITS = 8;
  localparam int BEDROCK_DECODE_FIELD_FORMAT_COUNT = 65;
  localparam int BEDROCK_DECODE_FIELD_FORMAT_ID_BITS = 7;
  localparam int BEDROCK_DECODE_EXT_ROOT_COUNT = 28;
  localparam int BEDROCK_DECODE_EXT_ROOT_BITS = 5;

  typedef enum logic [BEDROCK_DECODE_OPCODE_ID_BITS-1:0] {
    BR_OPCODE_INVALID = 8'd0,
    BR_OPCODE_ABS = 8'd1, // ABS
    BR_OPCODE_ADC = 8'd2, // ADC
    BR_OPCODE_ADD = 8'd3, // ADD
    BR_OPCODE_AFENCE = 8'd4, // AFENCE
    BR_OPCODE_AND = 8'd5, // AND
    BR_OPCODE_BCHG = 8'd6, // BCHG
    BR_OPCODE_BCLR = 8'd7, // BCLR
    BR_OPCODE_BKPT = 8'd8, // BKPT
    BR_OPCODE_BNDSII = 8'd9, // BNDSII
    BR_OPCODE_BNDSIX = 8'd10, // BNDSIX
    BR_OPCODE_BNDSXI = 8'd11, // BNDSXI
    BR_OPCODE_BNDSXX = 8'd12, // BNDSXX
    BR_OPCODE_BNDUII = 8'd13, // BNDUII
    BR_OPCODE_BNDUIX = 8'd14, // BNDUIX
    BR_OPCODE_BNDUXI = 8'd15, // BNDUXI
    BR_OPCODE_BNDUXX = 8'd16, // BNDUXX
    BR_OPCODE_BSET = 8'd17, // BSET
    BR_OPCODE_BTEST = 8'd18, // BTEST
    BR_OPCODE_CALL = 8'd19, // CALL
    BR_OPCODE_CLMUL = 8'd20, // CLMUL
    BR_OPCODE_CLMULH = 8'd21, // CLMULH
    BR_OPCODE_CLR = 8'd22, // CLR
    BR_OPCODE_CLS = 8'd23, // CLS
    BR_OPCODE_CLZ = 8'd24, // CLZ
    BR_OPCODE_CMP = 8'd25, // CMP
    BR_OPCODE_CMPXCHG = 8'd26, // CMPXCHG
    BR_OPCODE_CPUID = 8'd27, // CPUID
    BR_OPCODE_CTS = 8'd28, // CTS
    BR_OPCODE_CTZ = 8'd29, // CTZ
    BR_OPCODE_DEC = 8'd30, // DEC
    BR_OPCODE_DECN = 8'd31, // DECN
    BR_OPCODE_DIVMODS = 8'd32, // DIVMODS
    BR_OPCODE_DIVMODU = 8'd33, // DIVMODU
    BR_OPCODE_DIVS = 8'd34, // DIVS
    BR_OPCODE_DIVU = 8'd35, // DIVU
    BR_OPCODE_DJCC = 8'd36, // DJcc
    BR_OPCODE_ENCINST = 8'd37, // ENCINST
    BR_OPCODE_EXTSL = 8'd38, // EXTSL
    BR_OPCODE_EXTSQ = 8'd39, // EXTSQ
    BR_OPCODE_EXTSW = 8'd40, // EXTSW
    BR_OPCODE_EXTZL = 8'd41, // EXTZL
    BR_OPCODE_EXTZQ = 8'd42, // EXTZQ
    BR_OPCODE_EXTZW = 8'd43, // EXTZW
    BR_OPCODE_FABS = 8'd44, // FABS
    BR_OPCODE_FACOS = 8'd45, // FACOS
    BR_OPCODE_FADD = 8'd46, // FADD
    BR_OPCODE_FASIN = 8'd47, // FASIN
    BR_OPCODE_FATAN = 8'd48, // FATAN
    BR_OPCODE_FATANH = 8'd49, // FATANH
    BR_OPCODE_FBNDII = 8'd50, // FBNDII
    BR_OPCODE_FBNDIX = 8'd51, // FBNDIX
    BR_OPCODE_FBNDXI = 8'd52, // FBNDXI
    BR_OPCODE_FBNDXX = 8'd53, // FBNDXX
    BR_OPCODE_FCEIL = 8'd54, // FCEIL
    BR_OPCODE_FCLASS = 8'd55, // FCLASS
    BR_OPCODE_FCLR = 8'd56, // FCLR
    BR_OPCODE_FCMP = 8'd57, // FCMP
    BR_OPCODE_FCOPYSIGN = 8'd58, // FCOPYSIGN
    BR_OPCODE_FCOS = 8'd59, // FCOS
    BR_OPCODE_FCOSH = 8'd60, // FCOSH
    BR_OPCODE_FCVT = 8'd61, // FCVT
    BR_OPCODE_FCVTU = 8'd62, // FCVTU
    BR_OPCODE_FDIV = 8'd63, // FDIV
    BR_OPCODE_FETCHADD = 8'd64, // FETCHADD
    BR_OPCODE_FETCHAND = 8'd65, // FETCHAND
    BR_OPCODE_FETCHOR = 8'd66, // FETCHOR
    BR_OPCODE_FETCHSUB = 8'd67, // FETCHSUB
    BR_OPCODE_FETCHXOR = 8'd68, // FETCHXOR
    BR_OPCODE_FETOX = 8'd69, // FETOX
    BR_OPCODE_FETOXM1 = 8'd70, // FETOXM1
    BR_OPCODE_FFLOOR = 8'd71, // FFLOOR
    BR_OPCODE_FGETEXP = 8'd72, // FGETEXP
    BR_OPCODE_FGETMAN = 8'd73, // FGETMAN
    BR_OPCODE_FINT = 8'd74, // FINT
    BR_OPCODE_FINTRZ = 8'd75, // FINTRZ
    BR_OPCODE_FLOG10 = 8'd76, // FLOG10
    BR_OPCODE_FLOG2 = 8'd77, // FLOG2
    BR_OPCODE_FLOGN = 8'd78, // FLOGN
    BR_OPCODE_FLOGNP1 = 8'd79, // FLOGNP1
    BR_OPCODE_FLSHDCACHE = 8'd80, // FLSHDCACHE
    BR_OPCODE_FMADD = 8'd81, // FMADD
    BR_OPCODE_FMAX = 8'd82, // FMAX
    BR_OPCODE_FMIN = 8'd83, // FMIN
    BR_OPCODE_FMOD = 8'd84, // FMOD
    BR_OPCODE_FMOV = 8'd85, // FMOV
    BR_OPCODE_FMOVCC = 8'd86, // FMOVcc
    BR_OPCODE_FMOVCR = 8'd87, // FMOVCR
    BR_OPCODE_FMSUB = 8'd88, // FMSUB
    BR_OPCODE_FMUL = 8'd89, // FMUL
    BR_OPCODE_FNEG = 8'd90, // FNEG
    BR_OPCODE_FNMADD = 8'd91, // FNMADD
    BR_OPCODE_FNMSUB = 8'd92, // FNMSUB
    BR_OPCODE_FPOPM = 8'd93, // FPOPM
    BR_OPCODE_FPUSHM = 8'd94, // FPUSHM
    BR_OPCODE_FREM = 8'd95, // FREM
    BR_OPCODE_FROUND = 8'd96, // FROUND
    BR_OPCODE_FSCALE = 8'd97, // FSCALE
    BR_OPCODE_FSIN = 8'd98, // FSIN
    BR_OPCODE_FSINCOS = 8'd99, // FSINCOS
    BR_OPCODE_FSINH = 8'd100, // FSINH
    BR_OPCODE_FSQRT = 8'd101, // FSQRT
    BR_OPCODE_FSUB = 8'd102, // FSUB
    BR_OPCODE_FTAN = 8'd103, // FTAN
    BR_OPCODE_FTANH = 8'd104, // FTANH
    BR_OPCODE_FTENTOX = 8'd105, // FTENTOX
    BR_OPCODE_FTEST = 8'd106, // FTEST
    BR_OPCODE_FTRUNC = 8'd107, // FTRUNC
    BR_OPCODE_FTWOTOX = 8'd108, // FTWOTOX
    BR_OPCODE_FXCHG = 8'd109, // FXCHG
    BR_OPCODE_GETDB = 8'd110, // GETDB
    BR_OPCODE_HALT = 8'd111, // HALT
    BR_OPCODE_IJCC = 8'd112, // IJcc
    BR_OPCODE_ILLEGAL = 8'd113, // ILLEGAL
    BR_OPCODE_INC = 8'd114, // INC
    BR_OPCODE_INCN = 8'd115, // INCN
    BR_OPCODE_INVASID = 8'd116, // INVASID
    BR_OPCODE_INVDCACHE = 8'd117, // INVDCACHE
    BR_OPCODE_INVICACHE = 8'd118, // INVICACHE
    BR_OPCODE_INVPAGE = 8'd119, // INVPAGE
    BR_OPCODE_INVTLB = 8'd120, // INVTLB
    BR_OPCODE_IRET = 8'd121, // IRET
    BR_OPCODE_JCC = 8'd122, // Jcc
    BR_OPCODE_JMP = 8'd123, // JMP
    BR_OPCODE_LCALL = 8'd124, // LCALL
    BR_OPCODE_LEA = 8'd125, // LEA
    BR_OPCODE_LJMP = 8'd126, // LJMP
    BR_OPCODE_LRET = 8'd127, // LRET
    BR_OPCODE_MADD = 8'd128, // MADD
    BR_OPCODE_MAXS = 8'd129, // MAXS
    BR_OPCODE_MAXU = 8'd130, // MAXU
    BR_OPCODE_MINS = 8'd131, // MINS
    BR_OPCODE_MINU = 8'd132, // MINU
    BR_OPCODE_MODS = 8'd133, // MODS
    BR_OPCODE_MODU = 8'd134, // MODU
    BR_OPCODE_MOV = 8'd135, // MOV
    BR_OPCODE_MOVCC = 8'd136, // MOVcc
    BR_OPCODE_MOVSETAD = 8'd137, // MOVSETAD
    BR_OPCODE_MOVSETDA = 8'd138, // MOVSETDA
    BR_OPCODE_MOVSETDD = 8'd139, // MOVSETDD
    BR_OPCODE_MSUB = 8'd140, // MSUB
    BR_OPCODE_MULHS = 8'd141, // MULHS
    BR_OPCODE_MULHSU = 8'd142, // MULHSU
    BR_OPCODE_MULHU = 8'd143, // MULHU
    BR_OPCODE_MULS = 8'd144, // MULS
    BR_OPCODE_MULU = 8'd145, // MULU
    BR_OPCODE_NEG = 8'd146, // NEG
    BR_OPCODE_NOP = 8'd147, // NOP
    BR_OPCODE_NOT = 8'd148, // NOT
    BR_OPCODE_OR = 8'd149, // OR
    BR_OPCODE_PARITY = 8'd150, // PARITY
    BR_OPCODE_POP = 8'd151, // POP
    BR_OPCODE_POPCNT = 8'd152, // POPCNT
    BR_OPCODE_POPM = 8'd153, // POPM
    BR_OPCODE_PREFETCH = 8'd154, // PREFETCH
    BR_OPCODE_PTATTR = 8'd155, // PTATTR
    BR_OPCODE_PTQUERY = 8'd156, // PTQUERY
    BR_OPCODE_PUSH = 8'd157, // PUSH
    BR_OPCODE_PUSHM = 8'd158, // PUSHM
    BR_OPCODE_RCL = 8'd159, // RCL
    BR_OPCODE_RCR = 8'd160, // RCR
    BR_OPCODE_RDCR = 8'd161, // RDCR
    BR_OPCODE_RDFLAGS = 8'd162, // RDFLAGS
    BR_OPCODE_RDFSTATUS = 8'd163, // RDFSTATUS
    BR_OPCODE_RDPMC = 8'd164, // RDPMC
    BR_OPCODE_RDPTC = 8'd165, // RDPTC
    BR_OPCODE_RDSEG = 8'd166, // RDSEG
    BR_OPCODE_RDSTATUS = 8'd167, // RDSTATUS
    BR_OPCODE_REPG = 8'd168, // REPG
    BR_OPCODE_RESET = 8'd169, // RESET
    BR_OPCODE_RESTORE = 8'd170, // RESTORE
    BR_OPCODE_RET = 8'd171, // RET
    BR_OPCODE_REVBIT = 8'd172, // REVBIT
    BR_OPCODE_REVBYTE = 8'd173, // REVBYTE
    BR_OPCODE_RFENCE = 8'd174, // RFENCE
    BR_OPCODE_ROL = 8'd175, // ROL
    BR_OPCODE_ROR = 8'd176, // ROR
    BR_OPCODE_SAR = 8'd177, // SAR
    BR_OPCODE_SAVE = 8'd178, // SAVE
    BR_OPCODE_SBB = 8'd179, // SBB
    BR_OPCODE_SEGLEA = 8'd180, // SEGLEA
    BR_OPCODE_SELDB = 8'd181, // SELDB
    BR_OPCODE_SETCC = 8'd182, // SETcc
    BR_OPCODE_SHL = 8'd183, // SHL
    BR_OPCODE_SHR = 8'd184, // SHR
    BR_OPCODE_SUB = 8'd185, // SUB
    BR_OPCODE_SUM = 8'd186, // SUM
    BR_OPCODE_SWPT = 8'd187, // SWPT
    BR_OPCODE_SWPTA = 8'd188, // SWPTA
    BR_OPCODE_SYNCCACHE = 8'd189, // SYNCCACHE
    BR_OPCODE_SYSCALL = 8'd190, // SYSCALL
    BR_OPCODE_SYSRET = 8'd191, // SYSRET
    BR_OPCODE_TEST = 8'd192, // TEST
    BR_OPCODE_TESTCANON = 8'd193, // TESTCANON
    BR_OPCODE_TRACE = 8'd194, // TRACE
    BR_OPCODE_TRAP = 8'd195, // TRAP
    BR_OPCODE_TRAPCC = 8'd196, // TRAPcc
    BR_OPCODE_VTOP = 8'd197, // VTOP
    BR_OPCODE_WAIT = 8'd198, // WAIT
    BR_OPCODE_WFENCE = 8'd199, // WFENCE
    BR_OPCODE_WRBKDCACHE = 8'd200, // WRBKDCACHE
    BR_OPCODE_WRCR = 8'd201, // WRCR
    BR_OPCODE_WRFLAGS = 8'd202, // WRFLAGS
    BR_OPCODE_WRFSTATUS = 8'd203, // WRFSTATUS
    BR_OPCODE_WRSEG = 8'd204, // WRSEG
    BR_OPCODE_WRSTATUS = 8'd205, // WRSTATUS
    BR_OPCODE_XCHG = 8'd206, // XCHG
    BR_OPCODE_XCHGSETAD = 8'd207, // XCHGSETAD
    BR_OPCODE_XCHGSETDA = 8'd208, // XCHGSETDA
    BR_OPCODE_XCHGSETDD = 8'd209, // XCHGSETDD
    BR_OPCODE_XOR = 8'd210, // XOR
    BR_OPCODE_YIELD = 8'd211 // YIELD
  } bedrock_opcode_id_e;

  typedef enum logic [BEDROCK_DECODE_FIELD_FORMAT_ID_BITS-1:0] {
    BR_FIELD_FORMAT_NONE = 7'd0,
    BR_FIELD_FORMAT_F001 = 7'd1, // AREG3@0:0
    BR_FIELD_FORMAT_F002 = 7'd2, // DBANK4@1:0
    BR_FIELD_FORMAT_F003 = 7'd3, // DREG3@0:0
    BR_FIELD_FORMAT_F004 = 7'd4, // DREG3@1:0
    BR_FIELD_FORMAT_F005 = 7'd5, // EA6@1:0
    BR_FIELD_FORMAT_F006 = 7'd6, // FREG4@1:0
    BR_FIELD_FORMAT_F007 = 7'd7, // IMM1616@2:0
    BR_FIELD_FORMAT_F008 = 7'd8, // WL1@0:4
    BR_FIELD_FORMAT_F009 = 7'd9, // condition4@0:0
    BR_FIELD_FORMAT_F010 = 7'd10, // fbitmap1616@2:0
    BR_FIELD_FORMAT_F011 = 7'd11, // DBANK4@1:0_bitmap1616@2:0
    BR_FIELD_FORMAT_F012 = 7'd12, // DREG3@0:0_BWLQ2@0:3
    BR_FIELD_FORMAT_F013 = 7'd13, // DREG3@0:0_DREG3@0:3
    BR_FIELD_FORMAT_F014 = 7'd14, // DREG3@0:0_WL1@0:3
    BR_FIELD_FORMAT_F015 = 7'd15, // DREG3@0:6_WL1@0:9
    BR_FIELD_FORMAT_F016 = 7'd16, // DREG3@1:0_CR16@2:0
    BR_FIELD_FORMAT_F017 = 7'd17, // DREG3@1:0_DREG3@1:3
    BR_FIELD_FORMAT_F018 = 7'd18, // DREG3@1:0_FREG4@1:3
    BR_FIELD_FORMAT_F019 = 7'd19, // DREG3@1:0_IMM1616@2:0
    BR_FIELD_FORMAT_F020 = 7'd20, // DREG3@1:0_SREG3@1:3
    BR_FIELD_FORMAT_F021 = 7'd21, // EA6@1:0_AREG3@1:6
    BR_FIELD_FORMAT_F022 = 7'd22, // EA6@1:0_BWLQ2@1:6
    BR_FIELD_FORMAT_F023 = 7'd23, // EA6@1:0_DREG3@1:6
    BR_FIELD_FORMAT_F024 = 7'd24, // EA6@1:0_EA6@1:6
    BR_FIELD_FORMAT_F025 = 7'd25, // EA6@1:0_S_D1@1:6
    BR_FIELD_FORMAT_F026 = 7'd26, // FREG4@1:0_FREG4@1:4
    BR_FIELD_FORMAT_F027 = 7'd27, // FREG4@1:0_IMM1616@2:0
    BR_FIELD_FORMAT_F028 = 7'd28, // FREG4@1:0_S_D1@1:4
    BR_FIELD_FORMAT_F029 = 7'd29, // SREG3@1:0_DREG3@1:3
    BR_FIELD_FORMAT_F030 = 7'd30, // WL1@1:0_EA6@1:1
    BR_FIELD_FORMAT_F031 = 7'd31, // condition4@0:0_WL1@0:4
    BR_FIELD_FORMAT_F032 = 7'd32, // AREG3@1:0_BWLQ2@1:3_bitmap1616@2:0
    BR_FIELD_FORMAT_F033 = 7'd33, // DBANK4@1:0_DBANK4@1:4_bitmap1616@2:0
    BR_FIELD_FORMAT_F034 = 7'd34, // DREG3@0:0_DREG3@0:3_BW1@0:6
    BR_FIELD_FORMAT_F035 = 7'd35, // DREG3@0:0_DREG3@0:3_BWL2@0:6
    BR_FIELD_FORMAT_F036 = 7'd36, // DREG3@0:0_DREG3@0:3_LQ1@0:6
    BR_FIELD_FORMAT_F037 = 7'd37, // DREG3@1:0_BWLQ2@1:3_bitmap1616@2:0
    BR_FIELD_FORMAT_F038 = 7'd38, // DREG3@1:0_DREG3@1:3_BW1@1:6
    BR_FIELD_FORMAT_F039 = 7'd39, // DREG3@1:0_DREG3@1:3_BWLQ2@1:6
    BR_FIELD_FORMAT_F040 = 7'd40, // DREG3@1:0_FREG4@1:3_S_D1@1:7
    BR_FIELD_FORMAT_F041 = 7'd41, // EA6@0:0_DREG3@0:6_LQ1@0:9
    BR_FIELD_FORMAT_F042 = 7'd42, // EA6@1:0_BWLQ2@1:6_IMM66@1:8
    BR_FIELD_FORMAT_F043 = 7'd43, // EA6@1:0_DREG3@1:6_BW1@1:9
    BR_FIELD_FORMAT_F044 = 7'd44, // EA6@1:0_DREG3@1:6_BWL2@1:9
    BR_FIELD_FORMAT_F045 = 7'd45, // EA6@1:0_DREG3@1:6_BWLQ2@1:9
    BR_FIELD_FORMAT_F046 = 7'd46, // EA6@1:0_EA6@1:6_BW1@1:12
    BR_FIELD_FORMAT_F047 = 7'd47, // EA6@1:0_EA6@1:6_BWL2@1:12
    BR_FIELD_FORMAT_F048 = 7'd48, // EA6@1:0_EA6@1:6_BWLQ2@1:12
    BR_FIELD_FORMAT_F049 = 7'd49, // EA6@1:0_FREG4@1:6_S_D1@1:10
    BR_FIELD_FORMAT_F050 = 7'd50, // EA6@1:0_selector66@1:6_BWLQ2@1:12
    BR_FIELD_FORMAT_F051 = 7'd51, // FREG4@1:0_FREG4@1:4_S_D1@1:8
    BR_FIELD_FORMAT_F052 = 7'd52, // condition4@0:0_EA6@1:0_BWLQ2@1:6
    BR_FIELD_FORMAT_F053 = 7'd53, // condition4@0:0_EA6@1:0_WL1@1:6
    BR_FIELD_FORMAT_F054 = 7'd54, // condition4@0:0_FREG4@1:0_FREG4@1:4
    BR_FIELD_FORMAT_F055 = 7'd55, // EA6@1:0_DREG3@1:6_DREG3@1:9_BWLQ2@1:12
    BR_FIELD_FORMAT_F056 = 7'd56, // EA6@2:0_DREG3@2:6_DREG3@2:9_BWLQ2@2:12
    BR_FIELD_FORMAT_F057 = 7'd57, // EA6@2:0_FREG4@2:6_FREG4@2:10_S_D1@2:14
    BR_FIELD_FORMAT_F058 = 7'd58, // FREG4@2:0_FREG4@2:4_FREG4@2:8_S_D1@2:12
    BR_FIELD_FORMAT_F059 = 7'd59, // condition4@0:0_EA6@1:0_AREG3@1:6_BWLQ2@1:9
    BR_FIELD_FORMAT_F060 = 7'd60, // condition4@0:0_EA6@1:0_DREG3@1:6_BWLQ2@1:9
    BR_FIELD_FORMAT_F061 = 7'd61, // condition4@0:0_EA6@1:0_FREG4@1:6_S_D1@1:10
    BR_FIELD_FORMAT_F062 = 7'd62, // memory_order3@2:0_EA6@2:3_DREG3@2:9_BWLQ2@2:12
    BR_FIELD_FORMAT_F063 = 7'd63, // BWLQ2@1:0_memory_order3@2:0_EA6@2:3_DREG3@2:9_DREG3@2:12
    BR_FIELD_FORMAT_F064 = 7'd64 // condition4@0:0_EA6@1:0_DREG3@1:6_DREG3@1:9_LQ1@1:12
  } bedrock_field_format_id_e;

  typedef enum logic [BEDROCK_DECODE_EXT_ROOT_BITS-1:0] {
    BR_EXT_ROOT_NONE = 5'd0,
    BR_EXT_ROOT_ATOMIC_MEMORY = 5'd1, // EXT.atomic_memory
    BR_EXT_ROOT_CACHE_HINT = 5'd2, // EXT.cache_hint
    BR_EXT_ROOT_CONDITIONAL_CONTROL_CC = 5'd3, // EXT.conditional_control.cc
    BR_EXT_ROOT_CONTROL_FLOW = 5'd4, // EXT.control_flow
    BR_EXT_ROOT_DATA_MOVEMENT = 5'd5, // EXT.data_movement
    BR_EXT_ROOT_DATA_REGISTER_BANKING = 5'd6, // EXT.data_register_banking
    BR_EXT_ROOT_EA_UTILITY = 5'd7, // EXT.ea_utility
    BR_EXT_ROOT_FPU_ARITHMETIC = 5'd8, // EXT.fpu_arithmetic
    BR_EXT_ROOT_FPU_ARITHMETIC_EA_WIDE = 5'd9, // EXT.fpu_arithmetic_ea_wide
    BR_EXT_ROOT_FPU_MOVE_COMPARE = 5'd10, // EXT.fpu_move_compare
    BR_EXT_ROOT_FPU_TRANSCENDENTAL = 5'd11, // EXT.fpu_transcendental
    BR_EXT_ROOT_INTEGER_ALU = 5'd12, // EXT.integer_alu
    BR_EXT_ROOT_INTEGER_ALU_CMP_EA_WIDE = 5'd13, // EXT.integer_alu_cmp_ea_wide
    BR_EXT_ROOT_INTEGER_ALU_IMM_EA_ARITH_WIDE = 5'd14, // EXT.integer_alu_imm_ea_arith_wide
    BR_EXT_ROOT_INTEGER_ALU_IMM_EA_LOGIC_WIDE = 5'd15, // EXT.integer_alu_imm_ea_logic_wide
    BR_EXT_ROOT_INTEGER_ALU_REG_EA_WIDE = 5'd16, // EXT.integer_alu_reg_ea_wide
    BR_EXT_ROOT_INTEGER_BITFIELD = 5'd17, // EXT.integer_bitfield
    BR_EXT_ROOT_INTEGER_BITFIELD_BIT_IMM = 5'd18, // EXT.integer_bitfield_bit_imm
    BR_EXT_ROOT_INTEGER_BITFIELD_ROTATE_IMM = 5'd19, // EXT.integer_bitfield_rotate_imm
    BR_EXT_ROOT_INTEGER_BITFIELD_SHIFT_IMM = 5'd20, // EXT.integer_bitfield_shift_imm
    BR_EXT_ROOT_INTEGER_BOUNDS_SIGNED = 5'd21, // EXT.integer_bounds_signed
    BR_EXT_ROOT_INTEGER_BOUNDS_UNSIGNED = 5'd22, // EXT.integer_bounds_unsigned
    BR_EXT_ROOT_INTEGER_EXTEND_EA_WIDE = 5'd23, // EXT.integer_extend_ea_wide
    BR_EXT_ROOT_INTEGER_MAC = 5'd24, // EXT.integer_mac
    BR_EXT_ROOT_INTEGER_MUL_DIV = 5'd25, // EXT.integer_mul_div
    BR_EXT_ROOT_SYSTEM_CORE = 5'd26, // EXT.system_core
    BR_EXT_ROOT_TLB_CACHE = 5'd27, // EXT.tlb_cache
    BR_EXT_ROOT_VIRTUALIZATION_ACCELERATION = 5'd28 // EXT.virtualization_acceleration
  } bedrock_ext_root_e;

  typedef struct packed {
    logic [3:0] token_words;
    logic [1:0] ea_present;
    logic [11:0] ea_value;
    word_t ea0_descriptor_word;
  } bedrock_decode_field_extract_t;

  typedef struct packed {
    logic valid;
    logic needs_extension;
    bedrock_opcode_id_e opcode_id;
    bedrock_field_format_id_e field_format_id;
    logic [3:0] required_words;
    bedrock_ext_root_e ext_root;
    logic repg_fast_candidate;
  } bedrock_primary_decode_t;

  typedef struct packed {
    logic valid;
    bedrock_opcode_id_e opcode_id;
    bedrock_field_format_id_e field_format_id;
    logic [3:0] required_words;
    logic repg_fast_candidate;
  } bedrock_extended_decode_t;

  function automatic bedrock_primary_decode_t bedrock_decode_primary_payload(input primary_payload_t payload);
    bedrock_primary_decode_t r;
    r = '0;
    r.opcode_id = BR_OPCODE_INVALID;
    r.field_format_id = BR_FIELD_FORMAT_NONE;
    r.required_words = 4'd1;
    r.ext_root = BR_EXT_ROOT_NONE;

    priority casez (payload)
      12'b0000_0000_0000: begin // HALT
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_HALT;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b0000_0000_0001: begin // CALL.IMM32
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CALL;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
        r.required_words = 4'd3;
      end
      12'b0000_0000_0010: begin // CALL.IMM64
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CALL;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
        r.required_words = 4'd5;
      end
      12'b0000_0000_0011: begin // CALL.IMM16
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CALL;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
        r.required_words = 4'd2;
      end
      12'b0000_0000_0100: begin // BKPT
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_BKPT;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b0000_0000_0101: begin // AFENCE
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_AFENCE;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b0000_0000_0110: begin // WFENCE
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_WFENCE;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b0000_0000_0111: begin // RFENCE
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_RFENCE;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b0000_0000_1???: begin // PUSH.D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_PUSH;
        r.field_format_id = BR_FIELD_FORMAT_F003;
      end
      12'b0000_0001_????: begin // AND.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_AND;
        r.field_format_id = BR_FIELD_FORMAT_F014;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0000_001?_????: begin // DEC.D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_DEC;
        r.field_format_id = BR_FIELD_FORMAT_F012;
      end
      12'b0000_01??_????: begin // EXTSW.D_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_EXTSW;
        r.field_format_id = BR_FIELD_FORMAT_F013;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0000_1???_????: begin // ADD.D_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F036;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0001_0???_????: begin // EXTSQ.D_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_EXTSQ;
        r.field_format_id = BR_FIELD_FORMAT_F035;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0001_10??_????: begin // EXTSQ.D_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_EXTSQ;
        r.field_format_id = BR_FIELD_FORMAT_F035;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0001_110?_????: begin // INC.D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_INC;
        r.field_format_id = BR_FIELD_FORMAT_F012;
      end
      12'b0001_111?_????: begin // ABS.D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ABS;
        r.field_format_id = BR_FIELD_FORMAT_F012;
      end
      12'b0010_0???_????: begin // EXTZQ.D_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_EXTZQ;
        r.field_format_id = BR_FIELD_FORMAT_F035;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0010_10??_????: begin // EXTZQ.D_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_EXTZQ;
        r.field_format_id = BR_FIELD_FORMAT_F035;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0010_110?_????: begin // DECN.D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_DECN;
        r.field_format_id = BR_FIELD_FORMAT_F012;
      end
      12'b0010_111?_????: begin // INCN.D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_INCN;
        r.field_format_id = BR_FIELD_FORMAT_F012;
      end
      12'b0011_0???_????: begin // AND.D_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_AND;
        r.field_format_id = BR_FIELD_FORMAT_F036;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0011_1???_????: begin // CMP.D_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F036;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_0000_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_0100_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_1000_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_1100_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_0000_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_0100_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_1000_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_1100_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_0000_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_0100_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_1000_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_1100_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_0000_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_0100_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_1000_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_1100_0000: begin // ADD.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ADD;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_0000_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_0100_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_1000_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_1100_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_0000_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_0100_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_1000_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_1100_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_0000_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_0100_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_1000_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_1100_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_0000_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_0100_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_1000_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_1100_0001: begin // CMP.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CMP;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_0000_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_0100_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_1000_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_1100_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_0000_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_0100_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_1000_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_1100_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_0000_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_0100_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_1000_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_1100_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_0000_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_0100_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_1000_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_1100_0010: begin // SUB.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_0000_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_0100_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_1000_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_1100_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_0000_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_0100_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_1000_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_1100_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_0000_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_0100_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_1000_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_1100_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_0000_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_0100_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_1000_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_1100_0011: begin // TEST.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F015;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_0000_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_0001_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_001?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_0100_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_0101_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_011?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_1000_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_1001_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_101?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_1100_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_1101_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0100_111?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_0000_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_0001_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_001?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_0100_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_0101_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_011?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_1000_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_1001_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_101?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_1100_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_1101_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0101_111?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_0000_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_0001_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_001?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_0100_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_0101_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_011?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_1000_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_1001_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_101?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_1100_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_1101_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0110_111?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_0000_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_0001_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_001?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_0100_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_0101_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_011?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_1000_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_1001_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_101?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_1100_1???: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_1101_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b0111_111?_????: begin // MOV.D_TO_EA
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b10??_????_????: begin // MOV.EA_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F041;
        r.repg_fast_candidate = 1'b1;
      end
      12'b1100_0???_????: begin // OR.D_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_OR;
        r.field_format_id = BR_FIELD_FORMAT_F036;
        r.repg_fast_candidate = 1'b1;
      end
      12'b1100_1???_????: begin // SUB.D_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SUB;
        r.field_format_id = BR_FIELD_FORMAT_F036;
        r.repg_fast_candidate = 1'b1;
      end
      12'b1101_0???_????: begin // TEST.D_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TEST;
        r.field_format_id = BR_FIELD_FORMAT_F036;
        r.repg_fast_candidate = 1'b1;
      end
      12'b1101_1???_????: begin // XOR.D_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_XOR;
        r.field_format_id = BR_FIELD_FORMAT_F036;
        r.repg_fast_candidate = 1'b1;
      end
      12'b1110_0???_????: begin // EXTZL.D_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_EXTZL;
        r.field_format_id = BR_FIELD_FORMAT_F034;
        r.repg_fast_candidate = 1'b1;
      end
      12'b1110_100?_????: begin // NEG.D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_NEG;
        r.field_format_id = BR_FIELD_FORMAT_F012;
      end
      12'b1110_101?_????: begin // NOT.D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_NOT;
        r.field_format_id = BR_FIELD_FORMAT_F012;
      end
      12'b1110_1100_0000: begin // JMP.IMM
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_JMP;
        r.field_format_id = BR_FIELD_FORMAT_F008;
        r.required_words = 4'd2;
      end
      12'b1110_1101_0000: begin // JMP.IMM
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_JMP;
        r.field_format_id = BR_FIELD_FORMAT_F008;
        r.required_words = 4'd2;
      end
      12'b1110_1100_001?: begin // Jcc.IMM
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_JCC;
        r.field_format_id = BR_FIELD_FORMAT_F031;
        r.required_words = 4'd2;
      end
      12'b1110_1100_01??: begin // Jcc.IMM
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_JCC;
        r.field_format_id = BR_FIELD_FORMAT_F031;
        r.required_words = 4'd2;
      end
      12'b1110_1100_1???: begin // Jcc.IMM
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_JCC;
        r.field_format_id = BR_FIELD_FORMAT_F031;
        r.required_words = 4'd2;
      end
      12'b1110_1101_001?: begin // Jcc.IMM
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_JCC;
        r.field_format_id = BR_FIELD_FORMAT_F031;
        r.required_words = 4'd2;
      end
      12'b1110_1101_01??: begin // Jcc.IMM
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_JCC;
        r.field_format_id = BR_FIELD_FORMAT_F031;
        r.required_words = 4'd2;
      end
      12'b1110_1101_1???: begin // Jcc.IMM
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_JCC;
        r.field_format_id = BR_FIELD_FORMAT_F031;
        r.required_words = 4'd2;
      end
      12'b1110_1100_0001: begin // SYSCALL
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SYSCALL;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b1110_1101_0001: begin // WAIT
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_WAIT;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b1110_1110_????: begin // OR.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_OR;
        r.field_format_id = BR_FIELD_FORMAT_F014;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b1110_1111_????: begin // XOR.IMM_TO_D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_XOR;
        r.field_format_id = BR_FIELD_FORMAT_F014;
        r.required_words = 4'd2;
        r.repg_fast_candidate = 1'b1;
      end
      12'b1111_0000_0???: begin // PUSH.A
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_PUSH;
        r.field_format_id = BR_FIELD_FORMAT_F001;
      end
      12'b1111_0000_1???: begin // POP.D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_POP;
        r.field_format_id = BR_FIELD_FORMAT_F003;
      end
      12'b1111_0001_0???: begin // POP.A
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_POP;
        r.field_format_id = BR_FIELD_FORMAT_F001;
      end
      12'b1111_0001_1???: begin // CLR.A
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CLR;
        r.field_format_id = BR_FIELD_FORMAT_F001;
      end
      12'b1111_0010_0???: begin // CLR.D
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_CLR;
        r.field_format_id = BR_FIELD_FORMAT_F003;
      end
      12'b1111_0010_1???: begin // MOV.IMM_TO_A
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOV;
        r.field_format_id = BR_FIELD_FORMAT_F001;
        r.required_words = 4'd5;
        r.repg_fast_candidate = 1'b1;
      end
      12'b1111_0011_0000: begin // RET
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_RET;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0011_0001: begin // YIELD
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_YIELD;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0011_0010: begin // PUSHM.BITMAP
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_PUSHM;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
        r.required_words = 4'd2;
      end
      12'b1111_0011_0011: begin // POPM.BITMAP
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_POPM;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
        r.required_words = 4'd2;
      end
      12'b1111_0011_0100: begin // MOVSETAD.BITMAP
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOVSETAD;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
        r.required_words = 4'd2;
      end
      12'b1111_0011_0101: begin // MOVSETDA.BITMAP
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_MOVSETDA;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
        r.required_words = 4'd2;
      end
      12'b1111_0011_0110: begin // XCHGSETAD.BITMAP
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_XCHGSETAD;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
        r.required_words = 4'd2;
      end
      12'b1111_0011_0111: begin // XCHGSETDA.BITMAP
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_XCHGSETDA;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
        r.required_words = 4'd2;
      end
      12'b1111_0011_1000: begin // RESET
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_RESET;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0011_1001: begin // SYSRET
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_SYSRET;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0011_1010: begin // IRET
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_IRET;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0011_1011: begin // TRACE.IMM
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_TRACE;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
        r.required_words = 4'd2;
      end
      12'b1111_0100_1111: begin // NOP
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_NOP;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0111_0???: begin // REPG.D_TO_IMM
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_REPG;
        r.field_format_id = BR_FIELD_FORMAT_F003;
        r.required_words = 4'd2;
      end
      12'b1111_1111_1111: begin // ILLEGAL
        r.valid = 1'b1;
        r.opcode_id = BR_OPCODE_ILLEGAL;
        r.field_format_id = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0110_0000: begin // EXT.atomic_memory
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_ATOMIC_MEMORY;
      end
      12'b1111_0110_0001: begin // EXT.cache_hint
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_CACHE_HINT;
      end
      12'b1111_0101_????: begin // EXT.conditional_control.cc
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_CONDITIONAL_CONTROL_CC;
      end
      12'b1111_0100_1101: begin // EXT.control_flow
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_CONTROL_FLOW;
      end
      12'b1111_0100_1010: begin // EXT.data_movement
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_DATA_MOVEMENT;
      end
      12'b1111_0100_1011: begin // EXT.data_register_banking
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_DATA_REGISTER_BANKING;
      end
      12'b1111_0100_1100: begin // EXT.ea_utility
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_EA_UTILITY;
      end
      12'b1111_0110_0111: begin // EXT.fpu_arithmetic
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_FPU_ARITHMETIC;
      end
      12'b1111_0110_0110: begin // EXT.fpu_arithmetic_ea_wide
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_FPU_ARITHMETIC_EA_WIDE;
      end
      12'b1111_0110_0101: begin // EXT.fpu_move_compare
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_FPU_MOVE_COMPARE;
      end
      12'b1111_0110_1000: begin // EXT.fpu_transcendental
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_FPU_TRANSCENDENTAL;
      end
      12'b1111_0011_1100: begin // EXT.integer_alu
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_ALU;
      end
      12'b1111_0100_0000: begin // EXT.integer_alu_cmp_ea_wide
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_ALU_CMP_EA_WIDE;
      end
      12'b1111_0011_1110: begin // EXT.integer_alu_imm_ea_arith_wide
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_ALU_IMM_EA_ARITH_WIDE;
      end
      12'b1111_0011_1111: begin // EXT.integer_alu_imm_ea_logic_wide
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_ALU_IMM_EA_LOGIC_WIDE;
      end
      12'b1111_0011_1101: begin // EXT.integer_alu_reg_ea_wide
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_ALU_REG_EA_WIDE;
      end
      12'b1111_0100_0110: begin // EXT.integer_bitfield
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_BITFIELD;
      end
      12'b1111_0100_0111: begin // EXT.integer_bitfield_bit_imm
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_BITFIELD_BIT_IMM;
      end
      12'b1111_0100_1000: begin // EXT.integer_bitfield_rotate_imm
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_BITFIELD_ROTATE_IMM;
      end
      12'b1111_0100_1001: begin // EXT.integer_bitfield_shift_imm
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_BITFIELD_SHIFT_IMM;
      end
      12'b1111_0100_0010: begin // EXT.integer_bounds_signed
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_BOUNDS_SIGNED;
      end
      12'b1111_0100_0011: begin // EXT.integer_bounds_unsigned
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_BOUNDS_UNSIGNED;
      end
      12'b1111_0100_0001: begin // EXT.integer_extend_ea_wide
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_EXTEND_EA_WIDE;
      end
      12'b1111_0100_0101: begin // EXT.integer_mac
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_MAC;
      end
      12'b1111_0100_0100: begin // EXT.integer_mul_div
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_INTEGER_MUL_DIV;
      end
      12'b1111_0110_0011: begin // EXT.system_core
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_SYSTEM_CORE;
      end
      12'b1111_0110_0010: begin // EXT.tlb_cache
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_TLB_CACHE;
      end
      12'b1111_0110_0100: begin // EXT.virtualization_acceleration
        r.valid = 1'b1;
        r.needs_extension = 1'b1;
        r.ext_root = BR_EXT_ROOT_VIRTUALIZATION_ACCELERATION;
      end
      default: begin
      end
    endcase

    return r;
  endfunction

  function automatic bedrock_extended_decode_t bedrock_decode_extended_opcode(
    input bedrock_ext_root_e ext_root,
    input logic [15:0] extension_word
  );
    bedrock_extended_decode_t r;
    r = '0;
    r.opcode_id = BR_OPCODE_INVALID;
    r.field_format_id = BR_FIELD_FORMAT_NONE;
    r.required_words = 4'd2;

    unique case (ext_root)
      BR_EXT_ROOT_ATOMIC_MEMORY: begin // EXT.atomic_memory
        unique casez (extension_word)
          16'b0000_0000_0000_00??: begin // CMPXCHG.D_TO_D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CMPXCHG;
            r.field_format_id = BR_FIELD_FORMAT_F063;
          end
          16'b0000_0000_0000_0100: begin // FETCHADD.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FETCHADD;
            r.field_format_id = BR_FIELD_FORMAT_F062;
          end
          16'b0000_0000_0000_0101: begin // FETCHAND.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FETCHAND;
            r.field_format_id = BR_FIELD_FORMAT_F062;
          end
          16'b0000_0000_0000_0110: begin // FETCHOR.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FETCHOR;
            r.field_format_id = BR_FIELD_FORMAT_F062;
          end
          16'b0000_0000_0000_0111: begin // FETCHSUB.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FETCHSUB;
            r.field_format_id = BR_FIELD_FORMAT_F062;
          end
          16'b0000_0000_0000_1000: begin // FETCHXOR.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FETCHXOR;
            r.field_format_id = BR_FIELD_FORMAT_F062;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_CACHE_HINT: begin // EXT.cache_hint
        unique casez (extension_word)
          16'b0000_0000_00??_????: begin // PREFETCH.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_PREFETCH;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_CONDITIONAL_CONTROL_CC: begin // EXT.conditional_control.cc
        if (extension_word <= 16'h07ff) begin // DJcc.D_TO_EA
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_DJCC;
          r.field_format_id = BR_FIELD_FORMAT_F060;
        end
        else if ((extension_word >= 16'h0800) && (extension_word <= 16'h08ff)) begin // FMOVcc.F_TO_F
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_FMOVCC;
          r.field_format_id = BR_FIELD_FORMAT_F054;
        end
        else if (extension_word == 16'h0900) begin // TRAP
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_TRAP;
          r.field_format_id = BR_FIELD_FORMAT_NONE;
        end
        else if (extension_word == 16'h0900) begin // TRAPcc
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_TRAPCC;
          r.field_format_id = BR_FIELD_FORMAT_F009;
        end
        else if ((extension_word >= 16'h0980) && (extension_word <= 16'h09ff)) begin // JMP.EA
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_JMP;
          r.field_format_id = BR_FIELD_FORMAT_F030;
        end
        else if ((extension_word >= 16'h0980) && (extension_word <= 16'h09ff)) begin // Jcc.EA
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_JCC;
          r.field_format_id = BR_FIELD_FORMAT_F053;
        end
        else if ((extension_word >= 16'h0a00) && (extension_word <= 16'h0aff)) begin // SETcc.EA
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_SETCC;
          r.field_format_id = BR_FIELD_FORMAT_F052;
        end
        else if ((extension_word >= 16'h1000) && (extension_word <= 16'h17ff)) begin // MOVcc.A_TO_EA
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_MOVCC;
          r.field_format_id = BR_FIELD_FORMAT_F059;
        end
        else if ((extension_word >= 16'h1800) && (extension_word <= 16'h1fff)) begin // MOVcc.D_TO_EA
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_MOVCC;
          r.field_format_id = BR_FIELD_FORMAT_F060;
        end
        else if ((extension_word >= 16'h2000) && (extension_word <= 16'h3fff)) begin // IJcc.D_TO_D_TO_EA
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_IJCC;
          r.field_format_id = BR_FIELD_FORMAT_F064;
        end
        else if ((extension_word >= 16'h4000) && (extension_word <= 16'h47ff)) begin // MOVcc.EA_TO_A
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_MOVCC;
          r.field_format_id = BR_FIELD_FORMAT_F059;
        end
        else if ((extension_word >= 16'h4800) && (extension_word <= 16'h4fff)) begin // MOVcc.EA_TO_D
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_MOVCC;
          r.field_format_id = BR_FIELD_FORMAT_F060;
        end
        else if ((extension_word >= 16'h5000) && (extension_word <= 16'h57ff)) begin // FMOVcc.EA_TO_F
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_FMOVCC;
          r.field_format_id = BR_FIELD_FORMAT_F061;
        end
        else if ((extension_word >= 16'h5800) && (extension_word <= 16'h5fff)) begin // FMOVcc.F_TO_EA
          r.valid = 1'b1;
          r.opcode_id = BR_OPCODE_FMOVCC;
          r.field_format_id = BR_FIELD_FORMAT_F061;
        end
      end
      BR_EXT_ROOT_CONTROL_FLOW: begin // EXT.control_flow
        unique casez (extension_word)
          16'b0000_0000_00??_????: begin // CALL.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CALL;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          16'b0000_0000_0100_0000: begin // LRET
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_LRET;
            r.field_format_id = BR_FIELD_FORMAT_NONE;
          end
          16'b0000_001?_????_????: begin // LCALL.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_LCALL;
            r.field_format_id = BR_FIELD_FORMAT_F023;
          end
          16'b0000_010?_????_????: begin // LJMP.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_LJMP;
            r.field_format_id = BR_FIELD_FORMAT_F023;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_DATA_MOVEMENT: begin // EXT.data_movement
        unique casez (extension_word)
          16'b0000_0???_????_????: begin // MOV.D_TO_EA_WIDE
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MOV;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_1???_????_????: begin // MOV.EA_TO_D_WIDE
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MOV;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0001_0???_????_????: begin // XCHG.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_XCHG;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0001_1???_????_????: begin // XCHG.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_XCHG;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b01??_????_????_????: begin // MOV.EA_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MOV;
            r.field_format_id = BR_FIELD_FORMAT_F048;
            r.repg_fast_candidate = 1'b1;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_DATA_REGISTER_BANKING: begin // EXT.data_register_banking
        unique casez (extension_word)
          16'b0000_0000_0000_0???: begin // GETDB.D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_GETDB;
            r.field_format_id = BR_FIELD_FORMAT_F004;
          end
          16'b0000_0000_0000_1???: begin // SELDB.D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SELDB;
            r.field_format_id = BR_FIELD_FORMAT_F004;
          end
          16'b0000_0000_0001_????: begin // MOVSETAD.DB_TO_BITMAP
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MOVSETAD;
            r.field_format_id = BR_FIELD_FORMAT_F011;
          end
          16'b0000_0000_0010_????: begin // MOVSETDA.DB_TO_BITMAP
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MOVSETDA;
            r.field_format_id = BR_FIELD_FORMAT_F011;
          end
          16'b0000_0000_0011_????: begin // SELDB.DB
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SELDB;
            r.field_format_id = BR_FIELD_FORMAT_F002;
          end
          16'b0000_0000_0100_????: begin // XCHGSETAD.DB_TO_BITMAP
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_XCHGSETAD;
            r.field_format_id = BR_FIELD_FORMAT_F011;
          end
          16'b0000_0000_0101_????: begin // XCHGSETDA.DB_TO_BITMAP
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_XCHGSETDA;
            r.field_format_id = BR_FIELD_FORMAT_F011;
          end
          16'b0000_0001_????_????: begin // MOVSETDD.DB_TO_DB_TO_BITMAP
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MOVSETDD;
            r.field_format_id = BR_FIELD_FORMAT_F033;
          end
          16'b0000_0010_????_????: begin // XCHGSETDD.DB_TO_DB_TO_BITMAP
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_XCHGSETDD;
            r.field_format_id = BR_FIELD_FORMAT_F033;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_EA_UTILITY: begin // EXT.ea_utility
        unique casez (extension_word)
          16'b0000_000?_????_????: begin // LEA.EA_TO_A
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_LEA;
            r.field_format_id = BR_FIELD_FORMAT_F021;
          end
          16'b0000_001?_????_????: begin // SEGLEA.EA_TO_A
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SEGLEA;
            r.field_format_id = BR_FIELD_FORMAT_F021;
          end
          16'b0000_0100_00??_????: begin // TESTCANON.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_TESTCANON;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_FPU_ARITHMETIC: begin // EXT.fpu_arithmetic
        unique casez (extension_word)
          16'b0000_000?_????_????: begin // FABS.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FABS;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0000_001?_????_????: begin // FADD.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FADD;
            r.field_format_id = BR_FIELD_FORMAT_F051;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0100_0000_0000: begin // FBNDII.F_TO_EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FBNDII;
            r.field_format_id = BR_FIELD_FORMAT_F057;
          end
          16'b0000_0100_0000_0001: begin // FBNDII.F_TO_F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FBNDII;
            r.field_format_id = BR_FIELD_FORMAT_F058;
          end
          16'b0000_0100_0000_0010: begin // FBNDIX.F_TO_EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FBNDIX;
            r.field_format_id = BR_FIELD_FORMAT_F057;
          end
          16'b0000_0100_0000_0011: begin // FBNDIX.F_TO_F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FBNDIX;
            r.field_format_id = BR_FIELD_FORMAT_F058;
          end
          16'b0000_0100_0000_0100: begin // FBNDXI.F_TO_EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FBNDXI;
            r.field_format_id = BR_FIELD_FORMAT_F057;
          end
          16'b0000_0100_0000_0101: begin // FBNDXI.F_TO_F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FBNDXI;
            r.field_format_id = BR_FIELD_FORMAT_F058;
          end
          16'b0000_0100_0000_0110: begin // FBNDXX.F_TO_EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FBNDXX;
            r.field_format_id = BR_FIELD_FORMAT_F057;
          end
          16'b0000_0100_0000_0111: begin // FBNDXX.F_TO_F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FBNDXX;
            r.field_format_id = BR_FIELD_FORMAT_F058;
          end
          16'b0000_0100_0000_1000: begin // FCOPYSIGN.F_TO_F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCOPYSIGN;
            r.field_format_id = BR_FIELD_FORMAT_F058;
          end
          16'b0000_0100_0000_1001: begin // FMADD.EA_TO_F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMADD;
            r.field_format_id = BR_FIELD_FORMAT_F057;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0100_0000_1010: begin // FMADD.F_TO_EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMADD;
            r.field_format_id = BR_FIELD_FORMAT_F057;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0100_0000_1011: begin // FMADD.F_TO_F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMADD;
            r.field_format_id = BR_FIELD_FORMAT_F058;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0100_0000_1100: begin // FMSUB.EA_TO_F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMSUB;
            r.field_format_id = BR_FIELD_FORMAT_F057;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0100_0000_1101: begin // FMSUB.F_TO_EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMSUB;
            r.field_format_id = BR_FIELD_FORMAT_F057;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0100_0000_1110: begin // FMSUB.F_TO_F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMSUB;
            r.field_format_id = BR_FIELD_FORMAT_F058;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0100_0000_1111: begin // FNMADD.EA_TO_F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FNMADD;
            r.field_format_id = BR_FIELD_FORMAT_F057;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0100_0001_????: begin // FCLR.F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCLR;
            r.field_format_id = BR_FIELD_FORMAT_F006;
          end
          16'b0000_0100_0010_0000: begin // FNMADD.F_TO_EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FNMADD;
            r.field_format_id = BR_FIELD_FORMAT_F057;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0100_0010_0001: begin // FNMADD.F_TO_F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FNMADD;
            r.field_format_id = BR_FIELD_FORMAT_F058;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0100_0010_0010: begin // FNMSUB.EA_TO_F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FNMSUB;
            r.field_format_id = BR_FIELD_FORMAT_F057;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0100_0010_0011: begin // FNMSUB.F_TO_EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FNMSUB;
            r.field_format_id = BR_FIELD_FORMAT_F057;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0100_0010_0100: begin // FNMSUB.F_TO_F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FNMSUB;
            r.field_format_id = BR_FIELD_FORMAT_F058;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0100_0010_0101: begin // FPOPM.BITMAP
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FPOPM;
            r.field_format_id = BR_FIELD_FORMAT_F010;
          end
          16'b0000_0100_0010_0110: begin // FPUSHM.BITMAP
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FPUSHM;
            r.field_format_id = BR_FIELD_FORMAT_F010;
          end
          16'b0000_0100_01??_????: begin // FCLR.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCLR;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          16'b0000_0101_????_????: begin // FXCHG.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FXCHG;
            r.field_format_id = BR_FIELD_FORMAT_F026;
          end
          16'b0000_011?_????_????: begin // FCEIL.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCEIL;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0000_1???_????_????: begin // FCEIL.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCEIL;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b0001_0???_????_????: begin // FCEIL.F_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCEIL;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b0001_1???_????_????: begin // FDIV.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FDIV;
            r.field_format_id = BR_FIELD_FORMAT_F049;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0010_000?_????_????: begin // FDIV.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FDIV;
            r.field_format_id = BR_FIELD_FORMAT_F051;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0010_001?_????_????: begin // FFLOOR.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FFLOOR;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0010_010?_????_????: begin // FGETEXP.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FGETEXP;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0010_011?_????_????: begin // FGETMAN.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FGETMAN;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0010_1???_????_????: begin // FFLOOR.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FFLOOR;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b0011_0???_????_????: begin // FFLOOR.F_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FFLOOR;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b0011_1???_????_????: begin // FGETEXP.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FGETEXP;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b0100_0???_????_????: begin // FGETMAN.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FGETMAN;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b0100_1???_????_????: begin // FINT.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FINT;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b0101_0???_????_????: begin // FINT.F_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FINT;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b0101_100?_????_????: begin // FINT.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FINT;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0101_101?_????_????: begin // FINTRZ.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FINTRZ;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0101_110?_????_????: begin // FMAX.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMAX;
            r.field_format_id = BR_FIELD_FORMAT_F051;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0101_111?_????_????: begin // FMIN.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMIN;
            r.field_format_id = BR_FIELD_FORMAT_F051;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0110_0???_????_????: begin // FINTRZ.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FINTRZ;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b0110_1???_????_????: begin // FINTRZ.F_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FINTRZ;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b0111_0???_????_????: begin // FMAX.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMAX;
            r.field_format_id = BR_FIELD_FORMAT_F049;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0111_1???_????_????: begin // FMIN.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMIN;
            r.field_format_id = BR_FIELD_FORMAT_F049;
            r.repg_fast_candidate = 1'b1;
          end
          16'b1000_0???_????_????: begin // FMOD.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMOD;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b1000_100?_????_????: begin // FMOD.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMOD;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b1000_101?_????_????: begin // FMUL.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMUL;
            r.field_format_id = BR_FIELD_FORMAT_F051;
            r.repg_fast_candidate = 1'b1;
          end
          16'b1000_110?_????_????: begin // FNEG.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FNEG;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b1000_111?_????_????: begin // FREM.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FREM;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b1001_0???_????_????: begin // FMUL.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMUL;
            r.field_format_id = BR_FIELD_FORMAT_F049;
            r.repg_fast_candidate = 1'b1;
          end
          16'b1001_1???_????_????: begin // FNEG.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FNEG;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b1010_0???_????_????: begin // FNEG.F_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FNEG;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b1010_1???_????_????: begin // FREM.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FREM;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b1011_0???_????_????: begin // FROUND.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FROUND;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b1011_1???_????_????: begin // FROUND.F_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FROUND;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b1100_000?_????_????: begin // FROUND.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FROUND;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b1100_001?_????_????: begin // FSCALE.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FSCALE;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b1100_010?_????_????: begin // FSQRT.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FSQRT;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b1100_011?_????_????: begin // FSUB.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FSUB;
            r.field_format_id = BR_FIELD_FORMAT_F051;
            r.repg_fast_candidate = 1'b1;
          end
          16'b1100_1???_????_????: begin // FSCALE.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FSCALE;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b1101_0???_????_????: begin // FSQRT.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FSQRT;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b1101_1???_????_????: begin // FSQRT.F_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FSQRT;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b1110_0???_????_????: begin // FSUB.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FSUB;
            r.field_format_id = BR_FIELD_FORMAT_F049;
            r.repg_fast_candidate = 1'b1;
          end
          16'b1110_1???_????_????: begin // FTRUNC.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FTRUNC;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b1111_0???_????_????: begin // FTRUNC.F_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FTRUNC;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b1111_100?_????_????: begin // FTRUNC.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FTRUNC;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_FPU_ARITHMETIC_EA_WIDE: begin // EXT.fpu_arithmetic_ea_wide
        unique casez (extension_word)
          16'b0000_0???_????_????: begin // FABS.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FABS;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b0000_1???_????_????: begin // FABS.F_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FABS;
            r.field_format_id = BR_FIELD_FORMAT_F049;
          end
          16'b0001_0???_????_????: begin // FADD.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FADD;
            r.field_format_id = BR_FIELD_FORMAT_F049;
            r.repg_fast_candidate = 1'b1;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_FPU_MOVE_COMPARE: begin // EXT.fpu_move_compare
        unique casez (extension_word)
          16'b0000_000?_????_????: begin // FCMP.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCMP;
            r.field_format_id = BR_FIELD_FORMAT_F051;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0010_000?_????: begin // FTEST.F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FTEST;
            r.field_format_id = BR_FIELD_FORMAT_F028;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0010_0010_????: begin // FMOVCR.IMM_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMOVCR;
            r.field_format_id = BR_FIELD_FORMAT_F027;
          end
          16'b0000_0010_1???_????: begin // FCVT.D_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCVT;
            r.field_format_id = BR_FIELD_FORMAT_F018;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0011_????_????: begin // FCLASS.F_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCLASS;
            r.field_format_id = BR_FIELD_FORMAT_F040;
          end
          16'b0000_010?_????_????: begin // FMOV.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMOV;
            r.field_format_id = BR_FIELD_FORMAT_F051;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0110_0???_????: begin // FCVT.F_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCVT;
            r.field_format_id = BR_FIELD_FORMAT_F018;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0110_1???_????: begin // FCVTU.D_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCVTU;
            r.field_format_id = BR_FIELD_FORMAT_F018;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0111_????_????: begin // FCVT.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCVT;
            r.field_format_id = BR_FIELD_FORMAT_F026;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_1???_????_????: begin // FCMP.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCMP;
            r.field_format_id = BR_FIELD_FORMAT_F049;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0001_0000_0???_????: begin // FTEST.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FTEST;
            r.field_format_id = BR_FIELD_FORMAT_F025;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0001_0000_1???_????: begin // FCVTU.F_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCVTU;
            r.field_format_id = BR_FIELD_FORMAT_F018;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0001_0001_????_????: begin // FCVTU.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCVTU;
            r.field_format_id = BR_FIELD_FORMAT_F026;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0001_1???_????_????: begin // FMOV.EA_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMOV;
            r.field_format_id = BR_FIELD_FORMAT_F049;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0010_0???_????_????: begin // FMOV.F_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FMOV;
            r.field_format_id = BR_FIELD_FORMAT_F049;
            r.repg_fast_candidate = 1'b1;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_FPU_TRANSCENDENTAL: begin // EXT.fpu_transcendental
        unique casez (extension_word)
          16'b0000_000?_????_????: begin // FACOS.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FACOS;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0000_001?_????_????: begin // FASIN.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FASIN;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0000_010?_????_????: begin // FATAN.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FATAN;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0000_011?_????_????: begin // FATANH.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FATANH;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0000_100?_????_????: begin // FCOS.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCOS;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0000_101?_????_????: begin // FCOSH.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FCOSH;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0000_110?_????_????: begin // FETOX.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FETOX;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0000_111?_????_????: begin // FETOXM1.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FETOXM1;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0001_000?_????_????: begin // FLOG10.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FLOG10;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0001_001?_????_????: begin // FLOG2.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FLOG2;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0001_010?_????_????: begin // FLOGN.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FLOGN;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0001_011?_????_????: begin // FLOGNP1.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FLOGNP1;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0001_100?_????_????: begin // FSIN.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FSIN;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0001_101?_????_????: begin // FSINCOS.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FSINCOS;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0001_110?_????_????: begin // FSINH.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FSINH;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0001_111?_????_????: begin // FTAN.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FTAN;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0010_000?_????_????: begin // FTANH.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FTANH;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0010_001?_????_????: begin // FTENTOX.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FTENTOX;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          16'b0010_010?_????_????: begin // FTWOTOX.F_TO_F
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FTWOTOX;
            r.field_format_id = BR_FIELD_FORMAT_F051;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_ALU: begin // EXT.integer_alu
        unique casez (extension_word)
          16'b0000_0000_????_????: begin // ABS.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ABS;
            r.field_format_id = BR_FIELD_FORMAT_F022;
          end
          16'b0000_0001_00??_????: begin // CLR.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CLR;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          16'b0000_0001_010?_????: begin // SUM.BITMAP_TO_A
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SUM;
            r.field_format_id = BR_FIELD_FORMAT_F032;
          end
          16'b0000_0001_011?_????: begin // SUM.BITMAP_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SUM;
            r.field_format_id = BR_FIELD_FORMAT_F037;
          end
          16'b0000_0001_1???_????: begin // EXTSL.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTSL;
            r.field_format_id = BR_FIELD_FORMAT_F038;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_001?_????_????: begin // ADD.EA_TO_A
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ADD;
            r.field_format_id = BR_FIELD_FORMAT_F021;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_010?_????_????: begin // CMP.EA_TO_A
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CMP;
            r.field_format_id = BR_FIELD_FORMAT_F021;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0000_0110_????_????: begin // DEC.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_DEC;
            r.field_format_id = BR_FIELD_FORMAT_F022;
          end
          16'b0000_0111_????_????: begin // DECN.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_DECN;
            r.field_format_id = BR_FIELD_FORMAT_F022;
          end
          16'b0000_1???_????_????: begin // AND.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_AND;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0001_0???_????_????: begin // CMP.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CMP;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0001_1???_????_????: begin // CMP.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CMP;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0010_00??_????_????: begin // EXTSL.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTSL;
            r.field_format_id = BR_FIELD_FORMAT_F043;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0010_01??_????_????: begin // EXTSL.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTSL;
            r.field_format_id = BR_FIELD_FORMAT_F043;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0010_1???_????_????: begin // EXTSQ.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTSQ;
            r.field_format_id = BR_FIELD_FORMAT_F044;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0011_0???_????_????: begin // EXTSQ.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTSQ;
            r.field_format_id = BR_FIELD_FORMAT_F044;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0011_100?_????_????: begin // EXTSW.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTSW;
            r.field_format_id = BR_FIELD_FORMAT_F023;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0011_101?_????_????: begin // EXTSW.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTSW;
            r.field_format_id = BR_FIELD_FORMAT_F023;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0011_11??_????_????: begin // EXTZL.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTZL;
            r.field_format_id = BR_FIELD_FORMAT_F043;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0100_00??_????_????: begin // EXTZL.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTZL;
            r.field_format_id = BR_FIELD_FORMAT_F043;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0100_0100_????_????: begin // INC.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_INC;
            r.field_format_id = BR_FIELD_FORMAT_F022;
          end
          16'b0100_0101_????_????: begin // INCN.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_INCN;
            r.field_format_id = BR_FIELD_FORMAT_F022;
          end
          16'b0100_0110_????_????: begin // NEG.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_NEG;
            r.field_format_id = BR_FIELD_FORMAT_F022;
          end
          16'b0100_0111_????_????: begin // NOT.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_NOT;
            r.field_format_id = BR_FIELD_FORMAT_F022;
          end
          16'b0100_1???_????_????: begin // EXTZQ.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTZQ;
            r.field_format_id = BR_FIELD_FORMAT_F044;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0101_0???_????_????: begin // EXTZQ.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTZQ;
            r.field_format_id = BR_FIELD_FORMAT_F044;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0101_1???_????_????: begin // MAXS.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MAXS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0110_0???_????_????: begin // MAXS.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MAXS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0110_1???_????_????: begin // MAXU.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MAXU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0111_0???_????_????: begin // MAXU.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MAXU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0111_1???_????_????: begin // MINS.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MINS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1000_0???_????_????: begin // MINS.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MINS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1000_1???_????_????: begin // MINU.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MINU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1001_0???_????_????: begin // MINU.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MINU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1001_1???_????_????: begin // OR.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_OR;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b1010_0???_????_????: begin // OR.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_OR;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b1010_1000_????_????: begin // REVBYTE.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_REVBYTE;
            r.field_format_id = BR_FIELD_FORMAT_F039;
          end
          16'b1010_101?_????_????: begin // SUB.EA_TO_A
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SUB;
            r.field_format_id = BR_FIELD_FORMAT_F021;
            r.repg_fast_candidate = 1'b1;
          end
          16'b1011_0???_????_????: begin // REVBYTE.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_REVBYTE;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1011_1???_????_????: begin // REVBYTE.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_REVBYTE;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1100_0???_????_????: begin // SBB.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SBB;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1100_1???_????_????: begin // SBB.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SBB;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1101_0???_????_????: begin // SUB.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SUB;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b1101_1???_????_????: begin // SUB.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SUB;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b1110_0???_????_????: begin // TEST.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_TEST;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b1110_1???_????_????: begin // TEST.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_TEST;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b1111_0???_????_????: begin // XOR.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_XOR;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b1111_1???_????_????: begin // XOR.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_XOR;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_ALU_CMP_EA_WIDE: begin // EXT.integer_alu_cmp_ea_wide
        unique casez (extension_word)
          16'b00??_????_????_????: begin // CMP.EA_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CMP;
            r.field_format_id = BR_FIELD_FORMAT_F048;
            r.repg_fast_candidate = 1'b1;
          end
          16'b01??_????_????_????: begin // CMP.IMM_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CMP;
            r.field_format_id = BR_FIELD_FORMAT_F042;
            r.repg_fast_candidate = 1'b1;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_ALU_IMM_EA_ARITH_WIDE: begin // EXT.integer_alu_imm_ea_arith_wide
        unique casez (extension_word)
          16'b00??_????_????_????: begin // ADC.IMM_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ADC;
            r.field_format_id = BR_FIELD_FORMAT_F042;
          end
          16'b01??_????_????_????: begin // ADD.IMM_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ADD;
            r.field_format_id = BR_FIELD_FORMAT_F042;
            r.repg_fast_candidate = 1'b1;
          end
          16'b10??_????_????_????: begin // SBB.IMM_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SBB;
            r.field_format_id = BR_FIELD_FORMAT_F042;
          end
          16'b11??_????_????_????: begin // SUB.IMM_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SUB;
            r.field_format_id = BR_FIELD_FORMAT_F042;
            r.repg_fast_candidate = 1'b1;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_ALU_IMM_EA_LOGIC_WIDE: begin // EXT.integer_alu_imm_ea_logic_wide
        unique casez (extension_word)
          16'b00??_????_????_????: begin // AND.IMM_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_AND;
            r.field_format_id = BR_FIELD_FORMAT_F042;
            r.repg_fast_candidate = 1'b1;
          end
          16'b01??_????_????_????: begin // OR.IMM_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_OR;
            r.field_format_id = BR_FIELD_FORMAT_F042;
            r.repg_fast_candidate = 1'b1;
          end
          16'b10??_????_????_????: begin // TEST.IMM_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_TEST;
            r.field_format_id = BR_FIELD_FORMAT_F042;
            r.repg_fast_candidate = 1'b1;
          end
          16'b11??_????_????_????: begin // XOR.IMM_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_XOR;
            r.field_format_id = BR_FIELD_FORMAT_F042;
            r.repg_fast_candidate = 1'b1;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_ALU_REG_EA_WIDE: begin // EXT.integer_alu_reg_ea_wide
        unique casez (extension_word)
          16'b0000_0???_????_????: begin // ADC.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ADC;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0000_1???_????_????: begin // ADC.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ADC;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0001_0???_????_????: begin // ADD.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ADD;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0001_1???_????_????: begin // ADD.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ADD;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0010_0???_????_????: begin // AND.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_AND;
            r.field_format_id = BR_FIELD_FORMAT_F045;
            r.repg_fast_candidate = 1'b1;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_BITFIELD: begin // EXT.integer_bitfield
        unique casez (extension_word)
          16'b0000_0000_????_????: begin // BCHG.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BCHG;
            r.field_format_id = BR_FIELD_FORMAT_F039;
          end
          16'b0000_0001_????_????: begin // BCLR.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BCLR;
            r.field_format_id = BR_FIELD_FORMAT_F039;
          end
          16'b0000_0010_????_????: begin // BSET.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BSET;
            r.field_format_id = BR_FIELD_FORMAT_F039;
          end
          16'b0000_0011_????_????: begin // BTEST.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BTEST;
            r.field_format_id = BR_FIELD_FORMAT_F039;
          end
          16'b0000_0100_????_????: begin // PARITY.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_PARITY;
            r.field_format_id = BR_FIELD_FORMAT_F022;
          end
          16'b0000_0101_????_????: begin // RCL.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RCL;
            r.field_format_id = BR_FIELD_FORMAT_F039;
          end
          16'b0000_0110_????_????: begin // RCR.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RCR;
            r.field_format_id = BR_FIELD_FORMAT_F039;
          end
          16'b0000_0111_????_????: begin // REVBIT.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_REVBIT;
            r.field_format_id = BR_FIELD_FORMAT_F039;
          end
          16'b0000_1???_????_????: begin // BCHG.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BCHG;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0001_0???_????_????: begin // BCLR.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BCLR;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0001_1???_????_????: begin // BSET.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BSET;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0010_0???_????_????: begin // BTEST.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BTEST;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0010_1???_????_????: begin // CLS.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CLS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0011_0???_????_????: begin // CLZ.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CLZ;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0011_1???_????_????: begin // CTS.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CTS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0100_0???_????_????: begin // CTZ.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CTZ;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0100_1???_????_????: begin // POPCNT.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_POPCNT;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0101_0???_????_????: begin // RCL.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RCL;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0101_1???_????_????: begin // RCR.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RCR;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0110_0???_????_????: begin // REVBIT.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_REVBIT;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0110_1???_????_????: begin // REVBIT.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_REVBIT;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0111_0000_????_????: begin // ROL.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ROL;
            r.field_format_id = BR_FIELD_FORMAT_F039;
          end
          16'b0111_0001_????_????: begin // ROR.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ROR;
            r.field_format_id = BR_FIELD_FORMAT_F039;
          end
          16'b0111_0010_????_????: begin // SAR.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SAR;
            r.field_format_id = BR_FIELD_FORMAT_F039;
          end
          16'b0111_0011_????_????: begin // SHL.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SHL;
            r.field_format_id = BR_FIELD_FORMAT_F039;
          end
          16'b0111_0100_????_????: begin // SHR.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SHR;
            r.field_format_id = BR_FIELD_FORMAT_F039;
          end
          16'b0111_1???_????_????: begin // ROL.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ROL;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1000_0???_????_????: begin // ROR.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ROR;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1000_1???_????_????: begin // SAR.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SAR;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1001_0???_????_????: begin // SHL.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SHL;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1001_1???_????_????: begin // SHR.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SHR;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_BITFIELD_BIT_IMM: begin // EXT.integer_bitfield_bit_imm
        unique casez (extension_word)
          16'b00??_????_????_????: begin // BCHG.I6_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BCHG;
            r.field_format_id = BR_FIELD_FORMAT_F050;
          end
          16'b01??_????_????_????: begin // BCLR.I6_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BCLR;
            r.field_format_id = BR_FIELD_FORMAT_F050;
          end
          16'b10??_????_????_????: begin // BSET.I6_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BSET;
            r.field_format_id = BR_FIELD_FORMAT_F050;
          end
          16'b11??_????_????_????: begin // BTEST.I6_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BTEST;
            r.field_format_id = BR_FIELD_FORMAT_F050;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_BITFIELD_ROTATE_IMM: begin // EXT.integer_bitfield_rotate_imm
        unique casez (extension_word)
          16'b00??_????_????_????: begin // RCL.I6_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RCL;
            r.field_format_id = BR_FIELD_FORMAT_F050;
          end
          16'b01??_????_????_????: begin // RCR.I6_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RCR;
            r.field_format_id = BR_FIELD_FORMAT_F050;
          end
          16'b10??_????_????_????: begin // ROL.I6_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ROL;
            r.field_format_id = BR_FIELD_FORMAT_F050;
          end
          16'b11??_????_????_????: begin // ROR.I6_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ROR;
            r.field_format_id = BR_FIELD_FORMAT_F050;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_BITFIELD_SHIFT_IMM: begin // EXT.integer_bitfield_shift_imm
        unique casez (extension_word)
          16'b00??_????_????_????: begin // SHL.I6_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SHL;
            r.field_format_id = BR_FIELD_FORMAT_F050;
          end
          16'b01??_????_????_????: begin // SHR.I6_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SHR;
            r.field_format_id = BR_FIELD_FORMAT_F050;
          end
          16'b10??_????_????_????: begin // SAR.I6_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SAR;
            r.field_format_id = BR_FIELD_FORMAT_F050;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_BOUNDS_SIGNED: begin // EXT.integer_bounds_signed
        unique casez (extension_word)
          16'b00??_????_????_????: begin // BNDSII.D_TO_EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BNDSII;
            r.field_format_id = BR_FIELD_FORMAT_F055;
          end
          16'b01??_????_????_????: begin // BNDSIX.D_TO_EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BNDSIX;
            r.field_format_id = BR_FIELD_FORMAT_F055;
          end
          16'b10??_????_????_????: begin // BNDSXI.D_TO_EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BNDSXI;
            r.field_format_id = BR_FIELD_FORMAT_F055;
          end
          16'b11??_????_????_????: begin // BNDSXX.D_TO_EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BNDSXX;
            r.field_format_id = BR_FIELD_FORMAT_F055;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_BOUNDS_UNSIGNED: begin // EXT.integer_bounds_unsigned
        unique casez (extension_word)
          16'b00??_????_????_????: begin // BNDUII.D_TO_EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BNDUII;
            r.field_format_id = BR_FIELD_FORMAT_F055;
          end
          16'b01??_????_????_????: begin // BNDUIX.D_TO_EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BNDUIX;
            r.field_format_id = BR_FIELD_FORMAT_F055;
          end
          16'b10??_????_????_????: begin // BNDUXI.D_TO_EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BNDUXI;
            r.field_format_id = BR_FIELD_FORMAT_F055;
          end
          16'b11??_????_????_????: begin // BNDUXX.D_TO_EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_BNDUXX;
            r.field_format_id = BR_FIELD_FORMAT_F055;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_EXTEND_EA_WIDE: begin // EXT.integer_extend_ea_wide
        unique casez (extension_word)
          16'b000?_????_????_????: begin // EXTSL.EA_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTSL;
            r.field_format_id = BR_FIELD_FORMAT_F046;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0010_????_????_????: begin // EXTSW.EA_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTSW;
            r.field_format_id = BR_FIELD_FORMAT_F024;
            r.repg_fast_candidate = 1'b1;
          end
          16'b0011_????_????_????: begin // EXTZW.EA_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTZW;
            r.field_format_id = BR_FIELD_FORMAT_F024;
            r.repg_fast_candidate = 1'b1;
          end
          16'b01??_????_????_????: begin // EXTSQ.EA_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTSQ;
            r.field_format_id = BR_FIELD_FORMAT_F047;
            r.repg_fast_candidate = 1'b1;
          end
          16'b100?_????_????_????: begin // EXTZL.EA_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTZL;
            r.field_format_id = BR_FIELD_FORMAT_F046;
            r.repg_fast_candidate = 1'b1;
          end
          16'b11??_????_????_????: begin // EXTZQ.EA_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_EXTZQ;
            r.field_format_id = BR_FIELD_FORMAT_F047;
            r.repg_fast_candidate = 1'b1;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_MAC: begin // EXT.integer_mac
        unique casez (extension_word)
          16'b00??_????_????_????: begin // MADD.EA_TO_D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MADD;
            r.field_format_id = BR_FIELD_FORMAT_F055;
          end
          16'b01??_????_????_????: begin // MSUB.EA_TO_D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MSUB;
            r.field_format_id = BR_FIELD_FORMAT_F055;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_INTEGER_MUL_DIV: begin // EXT.integer_mul_div
        unique casez (extension_word)
          16'b0000_0???_????_????: begin // CLMUL.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CLMUL;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0000_1???_????_????: begin // CLMUL.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CLMUL;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0001_0???_????_????: begin // CLMULH.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CLMULH;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0001_1???_????_????: begin // CLMULH.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CLMULH;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0010_0000_0000_0000: begin // DIVMODS.EA_TO_D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_DIVMODS;
            r.field_format_id = BR_FIELD_FORMAT_F056;
          end
          16'b0010_1???_????_????: begin // DIVS.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_DIVS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0011_0???_????_????: begin // DIVS.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_DIVS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b0011_1???_????_????: begin // DIVU.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_DIVU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b01??_????_????_????: begin // DIVMODU.EA_TO_D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_DIVMODU;
            r.field_format_id = BR_FIELD_FORMAT_F055;
          end
          16'b1000_0???_????_????: begin // DIVU.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_DIVU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1000_1???_????_????: begin // MODS.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MODS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1001_0???_????_????: begin // MODS.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MODS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1001_1???_????_????: begin // MODU.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MODU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1010_0???_????_????: begin // MODU.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MODU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1010_1???_????_????: begin // MULHS.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MULHS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1011_0???_????_????: begin // MULHS.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MULHS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1011_1???_????_????: begin // MULHSU.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MULHSU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1100_0???_????_????: begin // MULHSU.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MULHSU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1100_1???_????_????: begin // MULHU.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MULHU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1101_0???_????_????: begin // MULHU.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MULHU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1101_1???_????_????: begin // MULS.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MULS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1110_0???_????_????: begin // MULS.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MULS;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1110_1???_????_????: begin // MULU.D_TO_EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MULU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          16'b1111_0???_????_????: begin // MULU.EA_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_MULU;
            r.field_format_id = BR_FIELD_FORMAT_F045;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_SYSTEM_CORE: begin // EXT.system_core
        unique casez (extension_word)
          16'b0000_0000_0000_0???: begin // RDCR.D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RDCR;
            r.field_format_id = BR_FIELD_FORMAT_F016;
          end
          16'b0000_0000_0000_1???: begin // WRCR.D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_WRCR;
            r.field_format_id = BR_FIELD_FORMAT_F016;
          end
          16'b0000_0000_0001_0???: begin // RDFLAGS.D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RDFLAGS;
            r.field_format_id = BR_FIELD_FORMAT_F004;
          end
          16'b0000_0000_0001_1???: begin // WRFLAGS.D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_WRFLAGS;
            r.field_format_id = BR_FIELD_FORMAT_F004;
          end
          16'b0000_0000_0010_0???: begin // RDSTATUS.D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RDSTATUS;
            r.field_format_id = BR_FIELD_FORMAT_F004;
          end
          16'b0000_0000_0010_1???: begin // WRSTATUS.D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_WRSTATUS;
            r.field_format_id = BR_FIELD_FORMAT_F004;
          end
          16'b0000_0000_0011_0???: begin // CPUID.D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_CPUID;
            r.field_format_id = BR_FIELD_FORMAT_F004;
          end
          16'b0000_0000_0011_1???: begin // RDFSTATUS.D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RDFSTATUS;
            r.field_format_id = BR_FIELD_FORMAT_F004;
          end
          16'b0000_0000_01??_????: begin // RDSEG.S_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RDSEG;
            r.field_format_id = BR_FIELD_FORMAT_F029;
          end
          16'b0000_0000_10??_????: begin // WRSEG.D_TO_S
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_WRSEG;
            r.field_format_id = BR_FIELD_FORMAT_F020;
          end
          16'b0000_0000_11??_????: begin // SAVE.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SAVE;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          16'b0000_0001_00??_????: begin // RESTORE.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RESTORE;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          16'b0000_0001_0100_0???: begin // RDPMC.IMM_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RDPMC;
            r.field_format_id = BR_FIELD_FORMAT_F019;
          end
          16'b0000_0001_0100_1???: begin // WRFSTATUS.D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_WRFSTATUS;
            r.field_format_id = BR_FIELD_FORMAT_F004;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_TLB_CACHE: begin // EXT.tlb_cache
        unique casez (extension_word)
          16'b0000_0000_0000_0000: begin // INVTLB
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_INVTLB;
            r.field_format_id = BR_FIELD_FORMAT_NONE;
          end
          16'b0000_0000_0000_0001: begin // INVASID.IMM
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_INVASID;
            r.field_format_id = BR_FIELD_FORMAT_F007;
          end
          16'b0000_0000_0000_1???: begin // SWPT.D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SWPT;
            r.field_format_id = BR_FIELD_FORMAT_F004;
          end
          16'b0000_0000_0001_0???: begin // RDPTC.D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_RDPTC;
            r.field_format_id = BR_FIELD_FORMAT_F004;
          end
          16'b0000_0000_01??_????: begin // INVPAGE.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_INVPAGE;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          16'b0000_0000_10??_????: begin // SWPTA.D_TO_D
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SWPTA;
            r.field_format_id = BR_FIELD_FORMAT_F017;
          end
          16'b0000_0000_11??_????: begin // INVDCACHE.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_INVDCACHE;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          16'b0000_0001_00??_????: begin // WRBKDCACHE.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_WRBKDCACHE;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          16'b0000_0001_01??_????: begin // FLSHDCACHE.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_FLSHDCACHE;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          16'b0000_0001_10??_????: begin // INVICACHE.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_INVICACHE;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          16'b0000_0001_11??_????: begin // SYNCCACHE.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_SYNCCACHE;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          16'b0000_0010_00??_????: begin // PTATTR.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_PTATTR;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          16'b0000_0010_01??_????: begin // PTQUERY.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_PTQUERY;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          16'b0000_0010_10??_????: begin // VTOP.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_VTOP;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          default: begin
          end
        endcase
      end
      BR_EXT_ROOT_VIRTUALIZATION_ACCELERATION: begin // EXT.virtualization_acceleration
        unique casez (extension_word)
          16'b0000_0000_00??_????: begin // ENCINST.EA
            r.valid = 1'b1;
            r.opcode_id = BR_OPCODE_ENCINST;
            r.field_format_id = BR_FIELD_FORMAT_F005;
          end
          default: begin
          end
        endcase
      end
      default: begin
      end
    endcase

    return r;
  endfunction

  function automatic logic [3:0] bedrock_decode_field_format_token_words(
    input bedrock_field_format_id_e field_format_id
  );
    logic [3:0] r;
    r = 4'd1;
    unique case (field_format_id)
      BR_FIELD_FORMAT_F002: r = 4'd2; // DBANK4@1:0
      BR_FIELD_FORMAT_F004: r = 4'd2; // DREG3@1:0
      BR_FIELD_FORMAT_F005: r = 4'd2; // EA6@1:0
      BR_FIELD_FORMAT_F006: r = 4'd2; // FREG4@1:0
      BR_FIELD_FORMAT_F007: r = 4'd3; // IMM1616@2:0
      BR_FIELD_FORMAT_F010: r = 4'd3; // fbitmap1616@2:0
      BR_FIELD_FORMAT_F011: r = 4'd3; // DBANK4@1:0_bitmap1616@2:0
      BR_FIELD_FORMAT_F016: r = 4'd3; // DREG3@1:0_CR16@2:0
      BR_FIELD_FORMAT_F017: r = 4'd2; // DREG3@1:0_DREG3@1:3
      BR_FIELD_FORMAT_F018: r = 4'd2; // DREG3@1:0_FREG4@1:3
      BR_FIELD_FORMAT_F019: r = 4'd3; // DREG3@1:0_IMM1616@2:0
      BR_FIELD_FORMAT_F020: r = 4'd2; // DREG3@1:0_SREG3@1:3
      BR_FIELD_FORMAT_F021: r = 4'd2; // EA6@1:0_AREG3@1:6
      BR_FIELD_FORMAT_F022: r = 4'd2; // EA6@1:0_BWLQ2@1:6
      BR_FIELD_FORMAT_F023: r = 4'd2; // EA6@1:0_DREG3@1:6
      BR_FIELD_FORMAT_F024: r = 4'd2; // EA6@1:0_EA6@1:6
      BR_FIELD_FORMAT_F025: r = 4'd2; // EA6@1:0_S_D1@1:6
      BR_FIELD_FORMAT_F026: r = 4'd2; // FREG4@1:0_FREG4@1:4
      BR_FIELD_FORMAT_F027: r = 4'd3; // FREG4@1:0_IMM1616@2:0
      BR_FIELD_FORMAT_F028: r = 4'd2; // FREG4@1:0_S_D1@1:4
      BR_FIELD_FORMAT_F029: r = 4'd2; // SREG3@1:0_DREG3@1:3
      BR_FIELD_FORMAT_F030: r = 4'd2; // WL1@1:0_EA6@1:1
      BR_FIELD_FORMAT_F032: r = 4'd3; // AREG3@1:0_BWLQ2@1:3_bitmap1616@2:0
      BR_FIELD_FORMAT_F033: r = 4'd3; // DBANK4@1:0_DBANK4@1:4_bitmap1616@2:0
      BR_FIELD_FORMAT_F037: r = 4'd3; // DREG3@1:0_BWLQ2@1:3_bitmap1616@2:0
      BR_FIELD_FORMAT_F038: r = 4'd2; // DREG3@1:0_DREG3@1:3_BW1@1:6
      BR_FIELD_FORMAT_F039: r = 4'd2; // DREG3@1:0_DREG3@1:3_BWLQ2@1:6
      BR_FIELD_FORMAT_F040: r = 4'd2; // DREG3@1:0_FREG4@1:3_S_D1@1:7
      BR_FIELD_FORMAT_F042: r = 4'd2; // EA6@1:0_BWLQ2@1:6_IMM66@1:8
      BR_FIELD_FORMAT_F043: r = 4'd2; // EA6@1:0_DREG3@1:6_BW1@1:9
      BR_FIELD_FORMAT_F044: r = 4'd2; // EA6@1:0_DREG3@1:6_BWL2@1:9
      BR_FIELD_FORMAT_F045: r = 4'd2; // EA6@1:0_DREG3@1:6_BWLQ2@1:9
      BR_FIELD_FORMAT_F046: r = 4'd2; // EA6@1:0_EA6@1:6_BW1@1:12
      BR_FIELD_FORMAT_F047: r = 4'd2; // EA6@1:0_EA6@1:6_BWL2@1:12
      BR_FIELD_FORMAT_F048: r = 4'd2; // EA6@1:0_EA6@1:6_BWLQ2@1:12
      BR_FIELD_FORMAT_F049: r = 4'd2; // EA6@1:0_FREG4@1:6_S_D1@1:10
      BR_FIELD_FORMAT_F050: r = 4'd2; // EA6@1:0_selector66@1:6_BWLQ2@1:12
      BR_FIELD_FORMAT_F051: r = 4'd2; // FREG4@1:0_FREG4@1:4_S_D1@1:8
      BR_FIELD_FORMAT_F052: r = 4'd2; // condition4@0:0_EA6@1:0_BWLQ2@1:6
      BR_FIELD_FORMAT_F053: r = 4'd2; // condition4@0:0_EA6@1:0_WL1@1:6
      BR_FIELD_FORMAT_F054: r = 4'd2; // condition4@0:0_FREG4@1:0_FREG4@1:4
      BR_FIELD_FORMAT_F055: r = 4'd2; // EA6@1:0_DREG3@1:6_DREG3@1:9_BWLQ2@1:12
      BR_FIELD_FORMAT_F056: r = 4'd3; // EA6@2:0_DREG3@2:6_DREG3@2:9_BWLQ2@2:12
      BR_FIELD_FORMAT_F057: r = 4'd3; // EA6@2:0_FREG4@2:6_FREG4@2:10_S_D1@2:14
      BR_FIELD_FORMAT_F058: r = 4'd3; // FREG4@2:0_FREG4@2:4_FREG4@2:8_S_D1@2:12
      BR_FIELD_FORMAT_F059: r = 4'd2; // condition4@0:0_EA6@1:0_AREG3@1:6_BWLQ2@1:9
      BR_FIELD_FORMAT_F060: r = 4'd2; // condition4@0:0_EA6@1:0_DREG3@1:6_BWLQ2@1:9
      BR_FIELD_FORMAT_F061: r = 4'd2; // condition4@0:0_EA6@1:0_FREG4@1:6_S_D1@1:10
      BR_FIELD_FORMAT_F062: r = 4'd3; // memory_order3@2:0_EA6@2:3_DREG3@2:9_BWLQ2@2:12
      BR_FIELD_FORMAT_F063: r = 4'd3; // BWLQ2@1:0_memory_order3@2:0_EA6@2:3_DREG3@2:9_DREG3@2:12
      BR_FIELD_FORMAT_F064: r = 4'd2; // condition4@0:0_EA6@1:0_DREG3@1:6_DREG3@1:9_LQ1@1:12
      default: begin
      end
    endcase
    return r;
  endfunction

  function automatic bedrock_decode_field_extract_t bedrock_decode_extract_fields(
    input bedrock_field_format_id_e field_format_id,
    input word_t token0_word,
    input word_t token1_word,
    input word_t token2_word,
    input word_t token3_word,
    input word_t token4_word,
    input word_t token5_word,
    input word_t token6_word,
    input word_t token7_word
  );
    bedrock_decode_field_extract_t r;
    r = '0;
    r.token_words = 4'd1;
    r.ea0_descriptor_word = word_t'(16'h0000);
    unique case (field_format_id)
      BR_FIELD_FORMAT_F001: begin // AREG3@0:0
        r.token_words = 4'd1;
      end
      BR_FIELD_FORMAT_F002: begin // DBANK4@1:0
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F003: begin // DREG3@0:0
        r.token_words = 4'd1;
      end
      BR_FIELD_FORMAT_F004: begin // DREG3@1:0
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F005: begin // EA6@1:0
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F006: begin // FREG4@1:0
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F007: begin // IMM1616@2:0
        r.token_words = 4'd3;
      end
      BR_FIELD_FORMAT_F008: begin // WL1@0:4
        r.token_words = 4'd1;
      end
      BR_FIELD_FORMAT_F009: begin // condition4@0:0
        r.token_words = 4'd1;
      end
      BR_FIELD_FORMAT_F010: begin // fbitmap1616@2:0
        r.token_words = 4'd3;
      end
      BR_FIELD_FORMAT_F011: begin // DBANK4@1:0_bitmap1616@2:0
        r.token_words = 4'd3;
      end
      BR_FIELD_FORMAT_F012: begin // DREG3@0:0_BWLQ2@0:3
        r.token_words = 4'd1;
      end
      BR_FIELD_FORMAT_F013: begin // DREG3@0:0_DREG3@0:3
        r.token_words = 4'd1;
      end
      BR_FIELD_FORMAT_F014: begin // DREG3@0:0_WL1@0:3
        r.token_words = 4'd1;
      end
      BR_FIELD_FORMAT_F015: begin // DREG3@0:6_WL1@0:9
        r.token_words = 4'd1;
      end
      BR_FIELD_FORMAT_F016: begin // DREG3@1:0_CR16@2:0
        r.token_words = 4'd3;
      end
      BR_FIELD_FORMAT_F017: begin // DREG3@1:0_DREG3@1:3
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F018: begin // DREG3@1:0_FREG4@1:3
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F019: begin // DREG3@1:0_IMM1616@2:0
        r.token_words = 4'd3;
      end
      BR_FIELD_FORMAT_F020: begin // DREG3@1:0_SREG3@1:3
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F021: begin // EA6@1:0_AREG3@1:6
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F022: begin // EA6@1:0_BWLQ2@1:6
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F023: begin // EA6@1:0_DREG3@1:6
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F024: begin // EA6@1:0_EA6@1:6
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
        r.ea_present[1] = 1'b1;
        r.ea_value[11:6] = token1_word[11:6];
      end
      BR_FIELD_FORMAT_F025: begin // EA6@1:0_S_D1@1:6
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F026: begin // FREG4@1:0_FREG4@1:4
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F027: begin // FREG4@1:0_IMM1616@2:0
        r.token_words = 4'd3;
      end
      BR_FIELD_FORMAT_F028: begin // FREG4@1:0_S_D1@1:4
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F029: begin // SREG3@1:0_DREG3@1:3
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F030: begin // WL1@1:0_EA6@1:1
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[6:1];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F031: begin // condition4@0:0_WL1@0:4
        r.token_words = 4'd1;
      end
      BR_FIELD_FORMAT_F032: begin // AREG3@1:0_BWLQ2@1:3_bitmap1616@2:0
        r.token_words = 4'd3;
      end
      BR_FIELD_FORMAT_F033: begin // DBANK4@1:0_DBANK4@1:4_bitmap1616@2:0
        r.token_words = 4'd3;
      end
      BR_FIELD_FORMAT_F034: begin // DREG3@0:0_DREG3@0:3_BW1@0:6
        r.token_words = 4'd1;
      end
      BR_FIELD_FORMAT_F035: begin // DREG3@0:0_DREG3@0:3_BWL2@0:6
        r.token_words = 4'd1;
      end
      BR_FIELD_FORMAT_F036: begin // DREG3@0:0_DREG3@0:3_LQ1@0:6
        r.token_words = 4'd1;
      end
      BR_FIELD_FORMAT_F037: begin // DREG3@1:0_BWLQ2@1:3_bitmap1616@2:0
        r.token_words = 4'd3;
      end
      BR_FIELD_FORMAT_F038: begin // DREG3@1:0_DREG3@1:3_BW1@1:6
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F039: begin // DREG3@1:0_DREG3@1:3_BWLQ2@1:6
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F040: begin // DREG3@1:0_FREG4@1:3_S_D1@1:7
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F041: begin // EA6@0:0_DREG3@0:6_LQ1@0:9
        r.token_words = 4'd1;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token0_word[5:0];
        r.ea0_descriptor_word = token1_word;
      end
      BR_FIELD_FORMAT_F042: begin // EA6@1:0_BWLQ2@1:6_IMM66@1:8
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F043: begin // EA6@1:0_DREG3@1:6_BW1@1:9
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F044: begin // EA6@1:0_DREG3@1:6_BWL2@1:9
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F045: begin // EA6@1:0_DREG3@1:6_BWLQ2@1:9
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F046: begin // EA6@1:0_EA6@1:6_BW1@1:12
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
        r.ea_present[1] = 1'b1;
        r.ea_value[11:6] = token1_word[11:6];
      end
      BR_FIELD_FORMAT_F047: begin // EA6@1:0_EA6@1:6_BWL2@1:12
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
        r.ea_present[1] = 1'b1;
        r.ea_value[11:6] = token1_word[11:6];
      end
      BR_FIELD_FORMAT_F048: begin // EA6@1:0_EA6@1:6_BWLQ2@1:12
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
        r.ea_present[1] = 1'b1;
        r.ea_value[11:6] = token1_word[11:6];
      end
      BR_FIELD_FORMAT_F049: begin // EA6@1:0_FREG4@1:6_S_D1@1:10
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F050: begin // EA6@1:0_selector66@1:6_BWLQ2@1:12
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F051: begin // FREG4@1:0_FREG4@1:4_S_D1@1:8
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F052: begin // condition4@0:0_EA6@1:0_BWLQ2@1:6
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F053: begin // condition4@0:0_EA6@1:0_WL1@1:6
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F054: begin // condition4@0:0_FREG4@1:0_FREG4@1:4
        r.token_words = 4'd2;
      end
      BR_FIELD_FORMAT_F055: begin // EA6@1:0_DREG3@1:6_DREG3@1:9_BWLQ2@1:12
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F056: begin // EA6@2:0_DREG3@2:6_DREG3@2:9_BWLQ2@2:12
        r.token_words = 4'd3;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token2_word[5:0];
        r.ea0_descriptor_word = token3_word;
      end
      BR_FIELD_FORMAT_F057: begin // EA6@2:0_FREG4@2:6_FREG4@2:10_S_D1@2:14
        r.token_words = 4'd3;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token2_word[5:0];
        r.ea0_descriptor_word = token3_word;
      end
      BR_FIELD_FORMAT_F058: begin // FREG4@2:0_FREG4@2:4_FREG4@2:8_S_D1@2:12
        r.token_words = 4'd3;
      end
      BR_FIELD_FORMAT_F059: begin // condition4@0:0_EA6@1:0_AREG3@1:6_BWLQ2@1:9
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F060: begin // condition4@0:0_EA6@1:0_DREG3@1:6_BWLQ2@1:9
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F061: begin // condition4@0:0_EA6@1:0_FREG4@1:6_S_D1@1:10
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      BR_FIELD_FORMAT_F062: begin // memory_order3@2:0_EA6@2:3_DREG3@2:9_BWLQ2@2:12
        r.token_words = 4'd3;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token2_word[8:3];
        r.ea0_descriptor_word = token3_word;
      end
      BR_FIELD_FORMAT_F063: begin // BWLQ2@1:0_memory_order3@2:0_EA6@2:3_DREG3@2:9_DREG3@2:12
        r.token_words = 4'd3;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token2_word[8:3];
        r.ea0_descriptor_word = token3_word;
      end
      BR_FIELD_FORMAT_F064: begin // condition4@0:0_EA6@1:0_DREG3@1:6_DREG3@1:9_LQ1@1:12
        r.token_words = 4'd2;
        r.ea_present[0] = 1'b1;
        r.ea_value[5:0] = token1_word[5:0];
        r.ea0_descriptor_word = token2_word;
      end
      default: begin
      end
    endcase
    return r;
  endfunction

  function automatic word_t bedrock_decode_ea1_descriptor_word(
    input bedrock_field_format_id_e field_format_id,
    input logic [2:0] ea0_payload_words,
    input word_t token0_word,
    input word_t token1_word,
    input word_t token2_word,
    input word_t token3_word,
    input word_t token4_word,
    input word_t token5_word,
    input word_t token6_word,
    input word_t token7_word
  );
    word_t r;
    r = word_t'(16'h0000);
    unique case (field_format_id)
      BR_FIELD_FORMAT_F024: begin // EA6@1:0_EA6@1:6
        unique case (ea0_payload_words)
          3'd0: r = token2_word;
          3'd1: r = token3_word;
          3'd2: r = token4_word;
          3'd3: r = token5_word;
          3'd4: r = token6_word;
          3'd5: r = token7_word;
          default: begin
          end
        endcase
      end
      BR_FIELD_FORMAT_F046: begin // EA6@1:0_EA6@1:6_BW1@1:12
        unique case (ea0_payload_words)
          3'd0: r = token2_word;
          3'd1: r = token3_word;
          3'd2: r = token4_word;
          3'd3: r = token5_word;
          3'd4: r = token6_word;
          3'd5: r = token7_word;
          default: begin
          end
        endcase
      end
      BR_FIELD_FORMAT_F047: begin // EA6@1:0_EA6@1:6_BWL2@1:12
        unique case (ea0_payload_words)
          3'd0: r = token2_word;
          3'd1: r = token3_word;
          3'd2: r = token4_word;
          3'd3: r = token5_word;
          3'd4: r = token6_word;
          3'd5: r = token7_word;
          default: begin
          end
        endcase
      end
      BR_FIELD_FORMAT_F048: begin // EA6@1:0_EA6@1:6_BWLQ2@1:12
        unique case (ea0_payload_words)
          3'd0: r = token2_word;
          3'd1: r = token3_word;
          3'd2: r = token4_word;
          3'd3: r = token5_word;
          3'd4: r = token6_word;
          3'd5: r = token7_word;
          default: begin
          end
        endcase
      end
      default: begin
      end
    endcase
    return r;
  endfunction

endpackage

`default_nettype wire
