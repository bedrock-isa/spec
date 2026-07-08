`timescale 1ns/1ps
`default_nettype none

// Package-free generated decoder for synthesis/statistics tools.
// The typed integration wrapper is build/generated/bedrock_decode.sv.

module bedrock_decode_synth(
  input  [11:0] primary_payload_i,
  input  [15:0] extension_word_i,
  output reg        valid_o,
  output reg        needs_extension_o,
  output reg [7:0] opcode_id_o,
  output reg [6:0] field_format_id_o,
  output reg [3:0]  required_words_o,
  output reg [4:0] ext_root_o,
  output reg        repg_fast_candidate_o
);

  localparam [7:0] BR_OPCODE_INVALID = 8'd0;
  localparam [7:0] BR_OPCODE_ABS = 8'd1; // ABS
  localparam [7:0] BR_OPCODE_ADC = 8'd2; // ADC
  localparam [7:0] BR_OPCODE_ADD = 8'd3; // ADD
  localparam [7:0] BR_OPCODE_AFENCE = 8'd4; // AFENCE
  localparam [7:0] BR_OPCODE_AND = 8'd5; // AND
  localparam [7:0] BR_OPCODE_BCHG = 8'd6; // BCHG
  localparam [7:0] BR_OPCODE_BCLR = 8'd7; // BCLR
  localparam [7:0] BR_OPCODE_BKPT = 8'd8; // BKPT
  localparam [7:0] BR_OPCODE_BNDSII = 8'd9; // BNDSII
  localparam [7:0] BR_OPCODE_BNDSIX = 8'd10; // BNDSIX
  localparam [7:0] BR_OPCODE_BNDSXI = 8'd11; // BNDSXI
  localparam [7:0] BR_OPCODE_BNDSXX = 8'd12; // BNDSXX
  localparam [7:0] BR_OPCODE_BNDUII = 8'd13; // BNDUII
  localparam [7:0] BR_OPCODE_BNDUIX = 8'd14; // BNDUIX
  localparam [7:0] BR_OPCODE_BNDUXI = 8'd15; // BNDUXI
  localparam [7:0] BR_OPCODE_BNDUXX = 8'd16; // BNDUXX
  localparam [7:0] BR_OPCODE_BSET = 8'd17; // BSET
  localparam [7:0] BR_OPCODE_BTEST = 8'd18; // BTEST
  localparam [7:0] BR_OPCODE_CALL = 8'd19; // CALL
  localparam [7:0] BR_OPCODE_CLMUL = 8'd20; // CLMUL
  localparam [7:0] BR_OPCODE_CLMULH = 8'd21; // CLMULH
  localparam [7:0] BR_OPCODE_CLR = 8'd22; // CLR
  localparam [7:0] BR_OPCODE_CLS = 8'd23; // CLS
  localparam [7:0] BR_OPCODE_CLZ = 8'd24; // CLZ
  localparam [7:0] BR_OPCODE_CMP = 8'd25; // CMP
  localparam [7:0] BR_OPCODE_CMPXCHG = 8'd26; // CMPXCHG
  localparam [7:0] BR_OPCODE_CPUID = 8'd27; // CPUID
  localparam [7:0] BR_OPCODE_CTS = 8'd28; // CTS
  localparam [7:0] BR_OPCODE_CTZ = 8'd29; // CTZ
  localparam [7:0] BR_OPCODE_DEC = 8'd30; // DEC
  localparam [7:0] BR_OPCODE_DECN = 8'd31; // DECN
  localparam [7:0] BR_OPCODE_DIVMODS = 8'd32; // DIVMODS
  localparam [7:0] BR_OPCODE_DIVMODU = 8'd33; // DIVMODU
  localparam [7:0] BR_OPCODE_DIVS = 8'd34; // DIVS
  localparam [7:0] BR_OPCODE_DIVU = 8'd35; // DIVU
  localparam [7:0] BR_OPCODE_DJCC = 8'd36; // DJcc
  localparam [7:0] BR_OPCODE_ENCINST = 8'd37; // ENCINST
  localparam [7:0] BR_OPCODE_EXTSL = 8'd38; // EXTSL
  localparam [7:0] BR_OPCODE_EXTSQ = 8'd39; // EXTSQ
  localparam [7:0] BR_OPCODE_EXTSW = 8'd40; // EXTSW
  localparam [7:0] BR_OPCODE_EXTZL = 8'd41; // EXTZL
  localparam [7:0] BR_OPCODE_EXTZQ = 8'd42; // EXTZQ
  localparam [7:0] BR_OPCODE_EXTZW = 8'd43; // EXTZW
  localparam [7:0] BR_OPCODE_FABS = 8'd44; // FABS
  localparam [7:0] BR_OPCODE_FACOS = 8'd45; // FACOS
  localparam [7:0] BR_OPCODE_FADD = 8'd46; // FADD
  localparam [7:0] BR_OPCODE_FASIN = 8'd47; // FASIN
  localparam [7:0] BR_OPCODE_FATAN = 8'd48; // FATAN
  localparam [7:0] BR_OPCODE_FATANH = 8'd49; // FATANH
  localparam [7:0] BR_OPCODE_FBNDII = 8'd50; // FBNDII
  localparam [7:0] BR_OPCODE_FBNDIX = 8'd51; // FBNDIX
  localparam [7:0] BR_OPCODE_FBNDXI = 8'd52; // FBNDXI
  localparam [7:0] BR_OPCODE_FBNDXX = 8'd53; // FBNDXX
  localparam [7:0] BR_OPCODE_FCEIL = 8'd54; // FCEIL
  localparam [7:0] BR_OPCODE_FCLASS = 8'd55; // FCLASS
  localparam [7:0] BR_OPCODE_FCLR = 8'd56; // FCLR
  localparam [7:0] BR_OPCODE_FCMP = 8'd57; // FCMP
  localparam [7:0] BR_OPCODE_FCOPYSIGN = 8'd58; // FCOPYSIGN
  localparam [7:0] BR_OPCODE_FCOS = 8'd59; // FCOS
  localparam [7:0] BR_OPCODE_FCOSH = 8'd60; // FCOSH
  localparam [7:0] BR_OPCODE_FCVT = 8'd61; // FCVT
  localparam [7:0] BR_OPCODE_FCVTU = 8'd62; // FCVTU
  localparam [7:0] BR_OPCODE_FDIV = 8'd63; // FDIV
  localparam [7:0] BR_OPCODE_FETCHADD = 8'd64; // FETCHADD
  localparam [7:0] BR_OPCODE_FETCHAND = 8'd65; // FETCHAND
  localparam [7:0] BR_OPCODE_FETCHOR = 8'd66; // FETCHOR
  localparam [7:0] BR_OPCODE_FETCHSUB = 8'd67; // FETCHSUB
  localparam [7:0] BR_OPCODE_FETCHXOR = 8'd68; // FETCHXOR
  localparam [7:0] BR_OPCODE_FETOX = 8'd69; // FETOX
  localparam [7:0] BR_OPCODE_FETOXM1 = 8'd70; // FETOXM1
  localparam [7:0] BR_OPCODE_FFLOOR = 8'd71; // FFLOOR
  localparam [7:0] BR_OPCODE_FGETEXP = 8'd72; // FGETEXP
  localparam [7:0] BR_OPCODE_FGETMAN = 8'd73; // FGETMAN
  localparam [7:0] BR_OPCODE_FINT = 8'd74; // FINT
  localparam [7:0] BR_OPCODE_FINTRZ = 8'd75; // FINTRZ
  localparam [7:0] BR_OPCODE_FLOG10 = 8'd76; // FLOG10
  localparam [7:0] BR_OPCODE_FLOG2 = 8'd77; // FLOG2
  localparam [7:0] BR_OPCODE_FLOGN = 8'd78; // FLOGN
  localparam [7:0] BR_OPCODE_FLOGNP1 = 8'd79; // FLOGNP1
  localparam [7:0] BR_OPCODE_FLSHDCACHE = 8'd80; // FLSHDCACHE
  localparam [7:0] BR_OPCODE_FMADD = 8'd81; // FMADD
  localparam [7:0] BR_OPCODE_FMAX = 8'd82; // FMAX
  localparam [7:0] BR_OPCODE_FMIN = 8'd83; // FMIN
  localparam [7:0] BR_OPCODE_FMOD = 8'd84; // FMOD
  localparam [7:0] BR_OPCODE_FMOV = 8'd85; // FMOV
  localparam [7:0] BR_OPCODE_FMOVCC = 8'd86; // FMOVcc
  localparam [7:0] BR_OPCODE_FMOVCR = 8'd87; // FMOVCR
  localparam [7:0] BR_OPCODE_FMSUB = 8'd88; // FMSUB
  localparam [7:0] BR_OPCODE_FMUL = 8'd89; // FMUL
  localparam [7:0] BR_OPCODE_FNEG = 8'd90; // FNEG
  localparam [7:0] BR_OPCODE_FNMADD = 8'd91; // FNMADD
  localparam [7:0] BR_OPCODE_FNMSUB = 8'd92; // FNMSUB
  localparam [7:0] BR_OPCODE_FPOPM = 8'd93; // FPOPM
  localparam [7:0] BR_OPCODE_FPUSHM = 8'd94; // FPUSHM
  localparam [7:0] BR_OPCODE_FREM = 8'd95; // FREM
  localparam [7:0] BR_OPCODE_FROUND = 8'd96; // FROUND
  localparam [7:0] BR_OPCODE_FSCALE = 8'd97; // FSCALE
  localparam [7:0] BR_OPCODE_FSIN = 8'd98; // FSIN
  localparam [7:0] BR_OPCODE_FSINCOS = 8'd99; // FSINCOS
  localparam [7:0] BR_OPCODE_FSINH = 8'd100; // FSINH
  localparam [7:0] BR_OPCODE_FSQRT = 8'd101; // FSQRT
  localparam [7:0] BR_OPCODE_FSUB = 8'd102; // FSUB
  localparam [7:0] BR_OPCODE_FTAN = 8'd103; // FTAN
  localparam [7:0] BR_OPCODE_FTANH = 8'd104; // FTANH
  localparam [7:0] BR_OPCODE_FTENTOX = 8'd105; // FTENTOX
  localparam [7:0] BR_OPCODE_FTEST = 8'd106; // FTEST
  localparam [7:0] BR_OPCODE_FTRUNC = 8'd107; // FTRUNC
  localparam [7:0] BR_OPCODE_FTWOTOX = 8'd108; // FTWOTOX
  localparam [7:0] BR_OPCODE_FXCHG = 8'd109; // FXCHG
  localparam [7:0] BR_OPCODE_GETDB = 8'd110; // GETDB
  localparam [7:0] BR_OPCODE_HALT = 8'd111; // HALT
  localparam [7:0] BR_OPCODE_IJCC = 8'd112; // IJcc
  localparam [7:0] BR_OPCODE_ILLEGAL = 8'd113; // ILLEGAL
  localparam [7:0] BR_OPCODE_INC = 8'd114; // INC
  localparam [7:0] BR_OPCODE_INCN = 8'd115; // INCN
  localparam [7:0] BR_OPCODE_INVASID = 8'd116; // INVASID
  localparam [7:0] BR_OPCODE_INVDCACHE = 8'd117; // INVDCACHE
  localparam [7:0] BR_OPCODE_INVICACHE = 8'd118; // INVICACHE
  localparam [7:0] BR_OPCODE_INVPAGE = 8'd119; // INVPAGE
  localparam [7:0] BR_OPCODE_INVTLB = 8'd120; // INVTLB
  localparam [7:0] BR_OPCODE_IRET = 8'd121; // IRET
  localparam [7:0] BR_OPCODE_JCC = 8'd122; // Jcc
  localparam [7:0] BR_OPCODE_JMP = 8'd123; // JMP
  localparam [7:0] BR_OPCODE_LCALL = 8'd124; // LCALL
  localparam [7:0] BR_OPCODE_LEA = 8'd125; // LEA
  localparam [7:0] BR_OPCODE_LJMP = 8'd126; // LJMP
  localparam [7:0] BR_OPCODE_LRET = 8'd127; // LRET
  localparam [7:0] BR_OPCODE_MADD = 8'd128; // MADD
  localparam [7:0] BR_OPCODE_MAXS = 8'd129; // MAXS
  localparam [7:0] BR_OPCODE_MAXU = 8'd130; // MAXU
  localparam [7:0] BR_OPCODE_MINS = 8'd131; // MINS
  localparam [7:0] BR_OPCODE_MINU = 8'd132; // MINU
  localparam [7:0] BR_OPCODE_MODS = 8'd133; // MODS
  localparam [7:0] BR_OPCODE_MODU = 8'd134; // MODU
  localparam [7:0] BR_OPCODE_MOV = 8'd135; // MOV
  localparam [7:0] BR_OPCODE_MOVCC = 8'd136; // MOVcc
  localparam [7:0] BR_OPCODE_MOVSETAD = 8'd137; // MOVSETAD
  localparam [7:0] BR_OPCODE_MOVSETDA = 8'd138; // MOVSETDA
  localparam [7:0] BR_OPCODE_MOVSETDD = 8'd139; // MOVSETDD
  localparam [7:0] BR_OPCODE_MSUB = 8'd140; // MSUB
  localparam [7:0] BR_OPCODE_MULHS = 8'd141; // MULHS
  localparam [7:0] BR_OPCODE_MULHSU = 8'd142; // MULHSU
  localparam [7:0] BR_OPCODE_MULHU = 8'd143; // MULHU
  localparam [7:0] BR_OPCODE_MULS = 8'd144; // MULS
  localparam [7:0] BR_OPCODE_MULU = 8'd145; // MULU
  localparam [7:0] BR_OPCODE_NEG = 8'd146; // NEG
  localparam [7:0] BR_OPCODE_NOP = 8'd147; // NOP
  localparam [7:0] BR_OPCODE_NOT = 8'd148; // NOT
  localparam [7:0] BR_OPCODE_OR = 8'd149; // OR
  localparam [7:0] BR_OPCODE_PARITY = 8'd150; // PARITY
  localparam [7:0] BR_OPCODE_POP = 8'd151; // POP
  localparam [7:0] BR_OPCODE_POPCNT = 8'd152; // POPCNT
  localparam [7:0] BR_OPCODE_POPM = 8'd153; // POPM
  localparam [7:0] BR_OPCODE_PREFETCH = 8'd154; // PREFETCH
  localparam [7:0] BR_OPCODE_PTATTR = 8'd155; // PTATTR
  localparam [7:0] BR_OPCODE_PTQUERY = 8'd156; // PTQUERY
  localparam [7:0] BR_OPCODE_PUSH = 8'd157; // PUSH
  localparam [7:0] BR_OPCODE_PUSHM = 8'd158; // PUSHM
  localparam [7:0] BR_OPCODE_RCL = 8'd159; // RCL
  localparam [7:0] BR_OPCODE_RCR = 8'd160; // RCR
  localparam [7:0] BR_OPCODE_RDCR = 8'd161; // RDCR
  localparam [7:0] BR_OPCODE_RDFLAGS = 8'd162; // RDFLAGS
  localparam [7:0] BR_OPCODE_RDFSTATUS = 8'd163; // RDFSTATUS
  localparam [7:0] BR_OPCODE_RDPMC = 8'd164; // RDPMC
  localparam [7:0] BR_OPCODE_RDPTC = 8'd165; // RDPTC
  localparam [7:0] BR_OPCODE_RDSEG = 8'd166; // RDSEG
  localparam [7:0] BR_OPCODE_RDSTATUS = 8'd167; // RDSTATUS
  localparam [7:0] BR_OPCODE_REPG = 8'd168; // REPG
  localparam [7:0] BR_OPCODE_RESET = 8'd169; // RESET
  localparam [7:0] BR_OPCODE_RESTORE = 8'd170; // RESTORE
  localparam [7:0] BR_OPCODE_RET = 8'd171; // RET
  localparam [7:0] BR_OPCODE_REVBIT = 8'd172; // REVBIT
  localparam [7:0] BR_OPCODE_REVBYTE = 8'd173; // REVBYTE
  localparam [7:0] BR_OPCODE_RFENCE = 8'd174; // RFENCE
  localparam [7:0] BR_OPCODE_ROL = 8'd175; // ROL
  localparam [7:0] BR_OPCODE_ROR = 8'd176; // ROR
  localparam [7:0] BR_OPCODE_SAR = 8'd177; // SAR
  localparam [7:0] BR_OPCODE_SAVE = 8'd178; // SAVE
  localparam [7:0] BR_OPCODE_SBB = 8'd179; // SBB
  localparam [7:0] BR_OPCODE_SEGLEA = 8'd180; // SEGLEA
  localparam [7:0] BR_OPCODE_SELDB = 8'd181; // SELDB
  localparam [7:0] BR_OPCODE_SETCC = 8'd182; // SETcc
  localparam [7:0] BR_OPCODE_SHL = 8'd183; // SHL
  localparam [7:0] BR_OPCODE_SHR = 8'd184; // SHR
  localparam [7:0] BR_OPCODE_SUB = 8'd185; // SUB
  localparam [7:0] BR_OPCODE_SUM = 8'd186; // SUM
  localparam [7:0] BR_OPCODE_SWPT = 8'd187; // SWPT
  localparam [7:0] BR_OPCODE_SWPTA = 8'd188; // SWPTA
  localparam [7:0] BR_OPCODE_SYNCCACHE = 8'd189; // SYNCCACHE
  localparam [7:0] BR_OPCODE_SYSCALL = 8'd190; // SYSCALL
  localparam [7:0] BR_OPCODE_SYSRET = 8'd191; // SYSRET
  localparam [7:0] BR_OPCODE_TEST = 8'd192; // TEST
  localparam [7:0] BR_OPCODE_TESTCANON = 8'd193; // TESTCANON
  localparam [7:0] BR_OPCODE_TRACE = 8'd194; // TRACE
  localparam [7:0] BR_OPCODE_TRAP = 8'd195; // TRAP
  localparam [7:0] BR_OPCODE_TRAPCC = 8'd196; // TRAPcc
  localparam [7:0] BR_OPCODE_VTOP = 8'd197; // VTOP
  localparam [7:0] BR_OPCODE_WAIT = 8'd198; // WAIT
  localparam [7:0] BR_OPCODE_WFENCE = 8'd199; // WFENCE
  localparam [7:0] BR_OPCODE_WRBKDCACHE = 8'd200; // WRBKDCACHE
  localparam [7:0] BR_OPCODE_WRCR = 8'd201; // WRCR
  localparam [7:0] BR_OPCODE_WRFLAGS = 8'd202; // WRFLAGS
  localparam [7:0] BR_OPCODE_WRFSTATUS = 8'd203; // WRFSTATUS
  localparam [7:0] BR_OPCODE_WRSEG = 8'd204; // WRSEG
  localparam [7:0] BR_OPCODE_WRSTATUS = 8'd205; // WRSTATUS
  localparam [7:0] BR_OPCODE_XCHG = 8'd206; // XCHG
  localparam [7:0] BR_OPCODE_XCHGSETAD = 8'd207; // XCHGSETAD
  localparam [7:0] BR_OPCODE_XCHGSETDA = 8'd208; // XCHGSETDA
  localparam [7:0] BR_OPCODE_XCHGSETDD = 8'd209; // XCHGSETDD
  localparam [7:0] BR_OPCODE_XOR = 8'd210; // XOR
  localparam [7:0] BR_OPCODE_YIELD = 8'd211; // YIELD

  localparam [6:0] BR_FIELD_FORMAT_NONE = 7'd0;
  localparam [6:0] BR_FIELD_FORMAT_F001 = 7'd1; // AREG3@0:0
  localparam [6:0] BR_FIELD_FORMAT_F002 = 7'd2; // DBANK4@1:0
  localparam [6:0] BR_FIELD_FORMAT_F003 = 7'd3; // DREG3@0:0
  localparam [6:0] BR_FIELD_FORMAT_F004 = 7'd4; // DREG3@1:0
  localparam [6:0] BR_FIELD_FORMAT_F005 = 7'd5; // EA6@1:0
  localparam [6:0] BR_FIELD_FORMAT_F006 = 7'd6; // FREG4@1:0
  localparam [6:0] BR_FIELD_FORMAT_F007 = 7'd7; // IMM1616@2:0
  localparam [6:0] BR_FIELD_FORMAT_F008 = 7'd8; // WL1@0:4
  localparam [6:0] BR_FIELD_FORMAT_F009 = 7'd9; // condition4@0:0
  localparam [6:0] BR_FIELD_FORMAT_F010 = 7'd10; // fbitmap1616@2:0
  localparam [6:0] BR_FIELD_FORMAT_F011 = 7'd11; // DBANK4@1:0_bitmap1616@2:0
  localparam [6:0] BR_FIELD_FORMAT_F012 = 7'd12; // DREG3@0:0_BWLQ2@0:3
  localparam [6:0] BR_FIELD_FORMAT_F013 = 7'd13; // DREG3@0:0_DREG3@0:3
  localparam [6:0] BR_FIELD_FORMAT_F014 = 7'd14; // DREG3@0:0_WL1@0:3
  localparam [6:0] BR_FIELD_FORMAT_F015 = 7'd15; // DREG3@0:6_WL1@0:9
  localparam [6:0] BR_FIELD_FORMAT_F016 = 7'd16; // DREG3@1:0_CR16@2:0
  localparam [6:0] BR_FIELD_FORMAT_F017 = 7'd17; // DREG3@1:0_DREG3@1:3
  localparam [6:0] BR_FIELD_FORMAT_F018 = 7'd18; // DREG3@1:0_FREG4@1:3
  localparam [6:0] BR_FIELD_FORMAT_F019 = 7'd19; // DREG3@1:0_IMM1616@2:0
  localparam [6:0] BR_FIELD_FORMAT_F020 = 7'd20; // DREG3@1:0_SREG3@1:3
  localparam [6:0] BR_FIELD_FORMAT_F021 = 7'd21; // EA6@1:0_AREG3@1:6
  localparam [6:0] BR_FIELD_FORMAT_F022 = 7'd22; // EA6@1:0_BWLQ2@1:6
  localparam [6:0] BR_FIELD_FORMAT_F023 = 7'd23; // EA6@1:0_DREG3@1:6
  localparam [6:0] BR_FIELD_FORMAT_F024 = 7'd24; // EA6@1:0_EA6@1:6
  localparam [6:0] BR_FIELD_FORMAT_F025 = 7'd25; // EA6@1:0_S_D1@1:6
  localparam [6:0] BR_FIELD_FORMAT_F026 = 7'd26; // FREG4@1:0_FREG4@1:4
  localparam [6:0] BR_FIELD_FORMAT_F027 = 7'd27; // FREG4@1:0_IMM1616@2:0
  localparam [6:0] BR_FIELD_FORMAT_F028 = 7'd28; // FREG4@1:0_S_D1@1:4
  localparam [6:0] BR_FIELD_FORMAT_F029 = 7'd29; // SREG3@1:0_DREG3@1:3
  localparam [6:0] BR_FIELD_FORMAT_F030 = 7'd30; // WL1@1:0_EA6@1:1
  localparam [6:0] BR_FIELD_FORMAT_F031 = 7'd31; // condition4@0:0_WL1@0:4
  localparam [6:0] BR_FIELD_FORMAT_F032 = 7'd32; // AREG3@1:0_BWLQ2@1:3_bitmap1616@2:0
  localparam [6:0] BR_FIELD_FORMAT_F033 = 7'd33; // DBANK4@1:0_DBANK4@1:4_bitmap1616@2:0
  localparam [6:0] BR_FIELD_FORMAT_F034 = 7'd34; // DREG3@0:0_DREG3@0:3_BW1@0:6
  localparam [6:0] BR_FIELD_FORMAT_F035 = 7'd35; // DREG3@0:0_DREG3@0:3_BWL2@0:6
  localparam [6:0] BR_FIELD_FORMAT_F036 = 7'd36; // DREG3@0:0_DREG3@0:3_LQ1@0:6
  localparam [6:0] BR_FIELD_FORMAT_F037 = 7'd37; // DREG3@1:0_BWLQ2@1:3_bitmap1616@2:0
  localparam [6:0] BR_FIELD_FORMAT_F038 = 7'd38; // DREG3@1:0_DREG3@1:3_BW1@1:6
  localparam [6:0] BR_FIELD_FORMAT_F039 = 7'd39; // DREG3@1:0_DREG3@1:3_BWLQ2@1:6
  localparam [6:0] BR_FIELD_FORMAT_F040 = 7'd40; // DREG3@1:0_FREG4@1:3_S_D1@1:7
  localparam [6:0] BR_FIELD_FORMAT_F041 = 7'd41; // EA6@0:0_DREG3@0:6_LQ1@0:9
  localparam [6:0] BR_FIELD_FORMAT_F042 = 7'd42; // EA6@1:0_BWLQ2@1:6_IMM66@1:8
  localparam [6:0] BR_FIELD_FORMAT_F043 = 7'd43; // EA6@1:0_DREG3@1:6_BW1@1:9
  localparam [6:0] BR_FIELD_FORMAT_F044 = 7'd44; // EA6@1:0_DREG3@1:6_BWL2@1:9
  localparam [6:0] BR_FIELD_FORMAT_F045 = 7'd45; // EA6@1:0_DREG3@1:6_BWLQ2@1:9
  localparam [6:0] BR_FIELD_FORMAT_F046 = 7'd46; // EA6@1:0_EA6@1:6_BW1@1:12
  localparam [6:0] BR_FIELD_FORMAT_F047 = 7'd47; // EA6@1:0_EA6@1:6_BWL2@1:12
  localparam [6:0] BR_FIELD_FORMAT_F048 = 7'd48; // EA6@1:0_EA6@1:6_BWLQ2@1:12
  localparam [6:0] BR_FIELD_FORMAT_F049 = 7'd49; // EA6@1:0_FREG4@1:6_S_D1@1:10
  localparam [6:0] BR_FIELD_FORMAT_F050 = 7'd50; // EA6@1:0_selector66@1:6_BWLQ2@1:12
  localparam [6:0] BR_FIELD_FORMAT_F051 = 7'd51; // FREG4@1:0_FREG4@1:4_S_D1@1:8
  localparam [6:0] BR_FIELD_FORMAT_F052 = 7'd52; // condition4@0:0_EA6@1:0_BWLQ2@1:6
  localparam [6:0] BR_FIELD_FORMAT_F053 = 7'd53; // condition4@0:0_EA6@1:0_WL1@1:6
  localparam [6:0] BR_FIELD_FORMAT_F054 = 7'd54; // condition4@0:0_FREG4@1:0_FREG4@1:4
  localparam [6:0] BR_FIELD_FORMAT_F055 = 7'd55; // EA6@1:0_DREG3@1:6_DREG3@1:9_BWLQ2@1:12
  localparam [6:0] BR_FIELD_FORMAT_F056 = 7'd56; // EA6@2:0_DREG3@2:6_DREG3@2:9_BWLQ2@2:12
  localparam [6:0] BR_FIELD_FORMAT_F057 = 7'd57; // EA6@2:0_FREG4@2:6_FREG4@2:10_S_D1@2:14
  localparam [6:0] BR_FIELD_FORMAT_F058 = 7'd58; // FREG4@2:0_FREG4@2:4_FREG4@2:8_S_D1@2:12
  localparam [6:0] BR_FIELD_FORMAT_F059 = 7'd59; // condition4@0:0_EA6@1:0_AREG3@1:6_BWLQ2@1:9
  localparam [6:0] BR_FIELD_FORMAT_F060 = 7'd60; // condition4@0:0_EA6@1:0_DREG3@1:6_BWLQ2@1:9
  localparam [6:0] BR_FIELD_FORMAT_F061 = 7'd61; // condition4@0:0_EA6@1:0_FREG4@1:6_S_D1@1:10
  localparam [6:0] BR_FIELD_FORMAT_F062 = 7'd62; // memory_order3@2:0_EA6@2:3_DREG3@2:9_BWLQ2@2:12
  localparam [6:0] BR_FIELD_FORMAT_F063 = 7'd63; // BWLQ2@1:0_memory_order3@2:0_EA6@2:3_DREG3@2:9_DREG3@2:12
  localparam [6:0] BR_FIELD_FORMAT_F064 = 7'd64; // condition4@0:0_EA6@1:0_DREG3@1:6_DREG3@1:9_LQ1@1:12

  localparam [4:0] BR_EXT_ROOT_NONE = 5'd0;
  localparam [4:0] BR_EXT_ROOT_ATOMIC_MEMORY = 5'd1; // EXT.atomic_memory
  localparam [4:0] BR_EXT_ROOT_CACHE_HINT = 5'd2; // EXT.cache_hint
  localparam [4:0] BR_EXT_ROOT_CONDITIONAL_CONTROL_CC = 5'd3; // EXT.conditional_control.cc
  localparam [4:0] BR_EXT_ROOT_CONTROL_FLOW = 5'd4; // EXT.control_flow
  localparam [4:0] BR_EXT_ROOT_DATA_MOVEMENT = 5'd5; // EXT.data_movement
  localparam [4:0] BR_EXT_ROOT_DATA_REGISTER_BANKING = 5'd6; // EXT.data_register_banking
  localparam [4:0] BR_EXT_ROOT_EA_UTILITY = 5'd7; // EXT.ea_utility
  localparam [4:0] BR_EXT_ROOT_FPU_ARITHMETIC = 5'd8; // EXT.fpu_arithmetic
  localparam [4:0] BR_EXT_ROOT_FPU_ARITHMETIC_EA_WIDE = 5'd9; // EXT.fpu_arithmetic_ea_wide
  localparam [4:0] BR_EXT_ROOT_FPU_MOVE_COMPARE = 5'd10; // EXT.fpu_move_compare
  localparam [4:0] BR_EXT_ROOT_FPU_TRANSCENDENTAL = 5'd11; // EXT.fpu_transcendental
  localparam [4:0] BR_EXT_ROOT_INTEGER_ALU = 5'd12; // EXT.integer_alu
  localparam [4:0] BR_EXT_ROOT_INTEGER_ALU_CMP_EA_WIDE = 5'd13; // EXT.integer_alu_cmp_ea_wide
  localparam [4:0] BR_EXT_ROOT_INTEGER_ALU_IMM_EA_ARITH_WIDE = 5'd14; // EXT.integer_alu_imm_ea_arith_wide
  localparam [4:0] BR_EXT_ROOT_INTEGER_ALU_IMM_EA_LOGIC_WIDE = 5'd15; // EXT.integer_alu_imm_ea_logic_wide
  localparam [4:0] BR_EXT_ROOT_INTEGER_ALU_REG_EA_WIDE = 5'd16; // EXT.integer_alu_reg_ea_wide
  localparam [4:0] BR_EXT_ROOT_INTEGER_BITFIELD = 5'd17; // EXT.integer_bitfield
  localparam [4:0] BR_EXT_ROOT_INTEGER_BITFIELD_BIT_IMM = 5'd18; // EXT.integer_bitfield_bit_imm
  localparam [4:0] BR_EXT_ROOT_INTEGER_BITFIELD_ROTATE_IMM = 5'd19; // EXT.integer_bitfield_rotate_imm
  localparam [4:0] BR_EXT_ROOT_INTEGER_BITFIELD_SHIFT_IMM = 5'd20; // EXT.integer_bitfield_shift_imm
  localparam [4:0] BR_EXT_ROOT_INTEGER_BOUNDS_SIGNED = 5'd21; // EXT.integer_bounds_signed
  localparam [4:0] BR_EXT_ROOT_INTEGER_BOUNDS_UNSIGNED = 5'd22; // EXT.integer_bounds_unsigned
  localparam [4:0] BR_EXT_ROOT_INTEGER_EXTEND_EA_WIDE = 5'd23; // EXT.integer_extend_ea_wide
  localparam [4:0] BR_EXT_ROOT_INTEGER_MAC = 5'd24; // EXT.integer_mac
  localparam [4:0] BR_EXT_ROOT_INTEGER_MUL_DIV = 5'd25; // EXT.integer_mul_div
  localparam [4:0] BR_EXT_ROOT_SYSTEM_CORE = 5'd26; // EXT.system_core
  localparam [4:0] BR_EXT_ROOT_TLB_CACHE = 5'd27; // EXT.tlb_cache
  localparam [4:0] BR_EXT_ROOT_VIRTUALIZATION_ACCELERATION = 5'd28; // EXT.virtualization_acceleration

  reg [3:0] field_format_token_words;

  always @* begin
    valid_o = 1'b0;
    needs_extension_o = 1'b0;
    opcode_id_o = BR_OPCODE_INVALID;
    field_format_id_o = BR_FIELD_FORMAT_NONE;
    required_words_o = 4'd0;
    ext_root_o = BR_EXT_ROOT_NONE;
    field_format_token_words = 4'd1;
    repg_fast_candidate_o = 1'b0;

    casez (primary_payload_i)
      12'b0000_0000_0000: begin // HALT
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_HALT;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b0000_0000_0001: begin // CALL.IMM32
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CALL;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
        required_words_o = 4'd3;
      end
      12'b0000_0000_0010: begin // CALL.IMM64
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CALL;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
        required_words_o = 4'd5;
      end
      12'b0000_0000_0011: begin // CALL.IMM16
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CALL;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
        required_words_o = 4'd2;
      end
      12'b0000_0000_0100: begin // BKPT
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_BKPT;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b0000_0000_0101: begin // AFENCE
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_AFENCE;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b0000_0000_0110: begin // WFENCE
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_WFENCE;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b0000_0000_0111: begin // RFENCE
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_RFENCE;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b0000_0000_1???: begin // PUSH.D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_PUSH;
        field_format_id_o = BR_FIELD_FORMAT_F003;
      end
      12'b0000_0001_????: begin // AND.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_AND;
        field_format_id_o = BR_FIELD_FORMAT_F014;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0000_001?_????: begin // DEC.D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_DEC;
        field_format_id_o = BR_FIELD_FORMAT_F012;
      end
      12'b0000_01??_????: begin // EXTSW.D_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_EXTSW;
        field_format_id_o = BR_FIELD_FORMAT_F013;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0000_1???_????: begin // ADD.D_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F036;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0001_0???_????: begin // EXTSQ.D_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_EXTSQ;
        field_format_id_o = BR_FIELD_FORMAT_F035;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0001_10??_????: begin // EXTSQ.D_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_EXTSQ;
        field_format_id_o = BR_FIELD_FORMAT_F035;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0001_110?_????: begin // INC.D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_INC;
        field_format_id_o = BR_FIELD_FORMAT_F012;
      end
      12'b0001_111?_????: begin // ABS.D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ABS;
        field_format_id_o = BR_FIELD_FORMAT_F012;
      end
      12'b0010_0???_????: begin // EXTZQ.D_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_EXTZQ;
        field_format_id_o = BR_FIELD_FORMAT_F035;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0010_10??_????: begin // EXTZQ.D_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_EXTZQ;
        field_format_id_o = BR_FIELD_FORMAT_F035;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0010_110?_????: begin // DECN.D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_DECN;
        field_format_id_o = BR_FIELD_FORMAT_F012;
      end
      12'b0010_111?_????: begin // INCN.D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_INCN;
        field_format_id_o = BR_FIELD_FORMAT_F012;
      end
      12'b0011_0???_????: begin // AND.D_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_AND;
        field_format_id_o = BR_FIELD_FORMAT_F036;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0011_1???_????: begin // CMP.D_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F036;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_0000_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_0100_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_1000_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_1100_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_0000_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_0100_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_1000_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_1100_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_0000_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_0100_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_1000_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_1100_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_0000_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_0100_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_1000_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_1100_0000: begin // ADD.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ADD;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_0000_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_0100_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_1000_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_1100_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_0000_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_0100_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_1000_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_1100_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_0000_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_0100_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_1000_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_1100_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_0000_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_0100_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_1000_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_1100_0001: begin // CMP.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CMP;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_0000_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_0100_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_1000_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_1100_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_0000_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_0100_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_1000_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_1100_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_0000_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_0100_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_1000_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_1100_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_0000_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_0100_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_1000_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_1100_0010: begin // SUB.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_0000_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_0100_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_1000_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_1100_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_0000_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_0100_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_1000_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_1100_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_0000_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_0100_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_1000_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_1100_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_0000_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_0100_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_1000_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_1100_0011: begin // TEST.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F015;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_0000_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_0001_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_001?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_0100_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_0101_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_011?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_1000_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_1001_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_101?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_1100_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_1101_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0100_111?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_0000_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_0001_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_001?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_0100_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_0101_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_011?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_1000_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_1001_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_101?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_1100_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_1101_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0101_111?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_0000_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_0001_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_001?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_0100_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_0101_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_011?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_1000_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_1001_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_101?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_1100_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_1101_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0110_111?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_0000_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_0001_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_001?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_0100_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_0101_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_011?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_1000_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_1001_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_101?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_1100_1???: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_1101_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b0111_111?_????: begin // MOV.D_TO_EA
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b10??_????_????: begin // MOV.EA_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F041;
        repg_fast_candidate_o = 1'b1;
      end
      12'b1100_0???_????: begin // OR.D_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_OR;
        field_format_id_o = BR_FIELD_FORMAT_F036;
        repg_fast_candidate_o = 1'b1;
      end
      12'b1100_1???_????: begin // SUB.D_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SUB;
        field_format_id_o = BR_FIELD_FORMAT_F036;
        repg_fast_candidate_o = 1'b1;
      end
      12'b1101_0???_????: begin // TEST.D_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TEST;
        field_format_id_o = BR_FIELD_FORMAT_F036;
        repg_fast_candidate_o = 1'b1;
      end
      12'b1101_1???_????: begin // XOR.D_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_XOR;
        field_format_id_o = BR_FIELD_FORMAT_F036;
        repg_fast_candidate_o = 1'b1;
      end
      12'b1110_0???_????: begin // EXTZL.D_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_EXTZL;
        field_format_id_o = BR_FIELD_FORMAT_F034;
        repg_fast_candidate_o = 1'b1;
      end
      12'b1110_100?_????: begin // NEG.D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_NEG;
        field_format_id_o = BR_FIELD_FORMAT_F012;
      end
      12'b1110_101?_????: begin // NOT.D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_NOT;
        field_format_id_o = BR_FIELD_FORMAT_F012;
      end
      12'b1110_1100_0000: begin // JMP.IMM
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_JMP;
        field_format_id_o = BR_FIELD_FORMAT_F008;
        required_words_o = 4'd2;
      end
      12'b1110_1101_0000: begin // JMP.IMM
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_JMP;
        field_format_id_o = BR_FIELD_FORMAT_F008;
        required_words_o = 4'd2;
      end
      12'b1110_1100_001?: begin // Jcc.IMM
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_JCC;
        field_format_id_o = BR_FIELD_FORMAT_F031;
        required_words_o = 4'd2;
      end
      12'b1110_1100_01??: begin // Jcc.IMM
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_JCC;
        field_format_id_o = BR_FIELD_FORMAT_F031;
        required_words_o = 4'd2;
      end
      12'b1110_1100_1???: begin // Jcc.IMM
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_JCC;
        field_format_id_o = BR_FIELD_FORMAT_F031;
        required_words_o = 4'd2;
      end
      12'b1110_1101_001?: begin // Jcc.IMM
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_JCC;
        field_format_id_o = BR_FIELD_FORMAT_F031;
        required_words_o = 4'd2;
      end
      12'b1110_1101_01??: begin // Jcc.IMM
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_JCC;
        field_format_id_o = BR_FIELD_FORMAT_F031;
        required_words_o = 4'd2;
      end
      12'b1110_1101_1???: begin // Jcc.IMM
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_JCC;
        field_format_id_o = BR_FIELD_FORMAT_F031;
        required_words_o = 4'd2;
      end
      12'b1110_1100_0001: begin // SYSCALL
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SYSCALL;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b1110_1101_0001: begin // WAIT
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_WAIT;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b1110_1110_????: begin // OR.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_OR;
        field_format_id_o = BR_FIELD_FORMAT_F014;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b1110_1111_????: begin // XOR.IMM_TO_D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_XOR;
        field_format_id_o = BR_FIELD_FORMAT_F014;
        required_words_o = 4'd2;
        repg_fast_candidate_o = 1'b1;
      end
      12'b1111_0000_0???: begin // PUSH.A
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_PUSH;
        field_format_id_o = BR_FIELD_FORMAT_F001;
      end
      12'b1111_0000_1???: begin // POP.D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_POP;
        field_format_id_o = BR_FIELD_FORMAT_F003;
      end
      12'b1111_0001_0???: begin // POP.A
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_POP;
        field_format_id_o = BR_FIELD_FORMAT_F001;
      end
      12'b1111_0001_1???: begin // CLR.A
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CLR;
        field_format_id_o = BR_FIELD_FORMAT_F001;
      end
      12'b1111_0010_0???: begin // CLR.D
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_CLR;
        field_format_id_o = BR_FIELD_FORMAT_F003;
      end
      12'b1111_0010_1???: begin // MOV.IMM_TO_A
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOV;
        field_format_id_o = BR_FIELD_FORMAT_F001;
        required_words_o = 4'd5;
        repg_fast_candidate_o = 1'b1;
      end
      12'b1111_0011_0000: begin // RET
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_RET;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0011_0001: begin // YIELD
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_YIELD;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0011_0010: begin // PUSHM.BITMAP
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_PUSHM;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
        required_words_o = 4'd2;
      end
      12'b1111_0011_0011: begin // POPM.BITMAP
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_POPM;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
        required_words_o = 4'd2;
      end
      12'b1111_0011_0100: begin // MOVSETAD.BITMAP
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOVSETAD;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
        required_words_o = 4'd2;
      end
      12'b1111_0011_0101: begin // MOVSETDA.BITMAP
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_MOVSETDA;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
        required_words_o = 4'd2;
      end
      12'b1111_0011_0110: begin // XCHGSETAD.BITMAP
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_XCHGSETAD;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
        required_words_o = 4'd2;
      end
      12'b1111_0011_0111: begin // XCHGSETDA.BITMAP
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_XCHGSETDA;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
        required_words_o = 4'd2;
      end
      12'b1111_0011_1000: begin // RESET
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_RESET;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0011_1001: begin // SYSRET
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_SYSRET;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0011_1010: begin // IRET
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_IRET;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0011_1011: begin // TRACE.IMM
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_TRACE;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
        required_words_o = 4'd2;
      end
      12'b1111_0100_1111: begin // NOP
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_NOP;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0111_0???: begin // REPG.D_TO_IMM
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_REPG;
        field_format_id_o = BR_FIELD_FORMAT_F003;
        required_words_o = 4'd2;
      end
      12'b1111_1111_1111: begin // ILLEGAL
        valid_o = 1'b1;
        opcode_id_o = BR_OPCODE_ILLEGAL;
        field_format_id_o = BR_FIELD_FORMAT_NONE;
      end
      12'b1111_0110_0000: begin // EXT.atomic_memory
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_ATOMIC_MEMORY;
      end
      12'b1111_0110_0001: begin // EXT.cache_hint
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_CACHE_HINT;
      end
      12'b1111_0101_????: begin // EXT.conditional_control.cc
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_CONDITIONAL_CONTROL_CC;
      end
      12'b1111_0100_1101: begin // EXT.control_flow
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_CONTROL_FLOW;
      end
      12'b1111_0100_1010: begin // EXT.data_movement
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_DATA_MOVEMENT;
      end
      12'b1111_0100_1011: begin // EXT.data_register_banking
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_DATA_REGISTER_BANKING;
      end
      12'b1111_0100_1100: begin // EXT.ea_utility
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_EA_UTILITY;
      end
      12'b1111_0110_0111: begin // EXT.fpu_arithmetic
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_FPU_ARITHMETIC;
      end
      12'b1111_0110_0110: begin // EXT.fpu_arithmetic_ea_wide
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_FPU_ARITHMETIC_EA_WIDE;
      end
      12'b1111_0110_0101: begin // EXT.fpu_move_compare
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_FPU_MOVE_COMPARE;
      end
      12'b1111_0110_1000: begin // EXT.fpu_transcendental
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_FPU_TRANSCENDENTAL;
      end
      12'b1111_0011_1100: begin // EXT.integer_alu
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_ALU;
      end
      12'b1111_0100_0000: begin // EXT.integer_alu_cmp_ea_wide
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_ALU_CMP_EA_WIDE;
      end
      12'b1111_0011_1110: begin // EXT.integer_alu_imm_ea_arith_wide
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_ALU_IMM_EA_ARITH_WIDE;
      end
      12'b1111_0011_1111: begin // EXT.integer_alu_imm_ea_logic_wide
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_ALU_IMM_EA_LOGIC_WIDE;
      end
      12'b1111_0011_1101: begin // EXT.integer_alu_reg_ea_wide
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_ALU_REG_EA_WIDE;
      end
      12'b1111_0100_0110: begin // EXT.integer_bitfield
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_BITFIELD;
      end
      12'b1111_0100_0111: begin // EXT.integer_bitfield_bit_imm
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_BITFIELD_BIT_IMM;
      end
      12'b1111_0100_1000: begin // EXT.integer_bitfield_rotate_imm
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_BITFIELD_ROTATE_IMM;
      end
      12'b1111_0100_1001: begin // EXT.integer_bitfield_shift_imm
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_BITFIELD_SHIFT_IMM;
      end
      12'b1111_0100_0010: begin // EXT.integer_bounds_signed
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_BOUNDS_SIGNED;
      end
      12'b1111_0100_0011: begin // EXT.integer_bounds_unsigned
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_BOUNDS_UNSIGNED;
      end
      12'b1111_0100_0001: begin // EXT.integer_extend_ea_wide
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_EXTEND_EA_WIDE;
      end
      12'b1111_0100_0101: begin // EXT.integer_mac
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_MAC;
      end
      12'b1111_0100_0100: begin // EXT.integer_mul_div
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_INTEGER_MUL_DIV;
      end
      12'b1111_0110_0011: begin // EXT.system_core
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_SYSTEM_CORE;
      end
      12'b1111_0110_0010: begin // EXT.tlb_cache
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_TLB_CACHE;
      end
      12'b1111_0110_0100: begin // EXT.virtualization_acceleration
        valid_o = 1'b1;
        needs_extension_o = 1'b1;
        ext_root_o = BR_EXT_ROOT_VIRTUALIZATION_ACCELERATION;
      end
      default: begin
      end
    endcase

    if (valid_o && required_words_o == 4'd0) begin
      required_words_o = 4'd1;
    end

    if (needs_extension_o) begin
      valid_o = 1'b0;
      opcode_id_o = BR_OPCODE_INVALID;
      field_format_id_o = BR_FIELD_FORMAT_NONE;
      required_words_o = 4'd2;

      case (ext_root_o)
        BR_EXT_ROOT_ATOMIC_MEMORY: begin // EXT.atomic_memory
          casez (extension_word_i)
            16'b0000_0000_0000_00??: begin // CMPXCHG.D_TO_D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CMPXCHG;
              field_format_id_o = BR_FIELD_FORMAT_F063;
            end
            16'b0000_0000_0000_0100: begin // FETCHADD.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FETCHADD;
              field_format_id_o = BR_FIELD_FORMAT_F062;
            end
            16'b0000_0000_0000_0101: begin // FETCHAND.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FETCHAND;
              field_format_id_o = BR_FIELD_FORMAT_F062;
            end
            16'b0000_0000_0000_0110: begin // FETCHOR.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FETCHOR;
              field_format_id_o = BR_FIELD_FORMAT_F062;
            end
            16'b0000_0000_0000_0111: begin // FETCHSUB.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FETCHSUB;
              field_format_id_o = BR_FIELD_FORMAT_F062;
            end
            16'b0000_0000_0000_1000: begin // FETCHXOR.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FETCHXOR;
              field_format_id_o = BR_FIELD_FORMAT_F062;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_CACHE_HINT: begin // EXT.cache_hint
          casez (extension_word_i)
            16'b0000_0000_00??_????: begin // PREFETCH.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_PREFETCH;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_CONDITIONAL_CONTROL_CC: begin // EXT.conditional_control.cc
          if (extension_word_i <= 16'h07ff) begin // DJcc.D_TO_EA
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_DJCC;
            field_format_id_o = BR_FIELD_FORMAT_F060;
          end
          else if ((extension_word_i >= 16'h0800) && (extension_word_i <= 16'h08ff)) begin // FMOVcc.F_TO_F
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_FMOVCC;
            field_format_id_o = BR_FIELD_FORMAT_F054;
          end
          else if (extension_word_i == 16'h0900) begin // TRAP
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_TRAP;
            field_format_id_o = BR_FIELD_FORMAT_NONE;
          end
          else if (extension_word_i == 16'h0900) begin // TRAPcc
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_TRAPCC;
            field_format_id_o = BR_FIELD_FORMAT_F009;
          end
          else if ((extension_word_i >= 16'h0980) && (extension_word_i <= 16'h09ff)) begin // JMP.EA
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_JMP;
            field_format_id_o = BR_FIELD_FORMAT_F030;
          end
          else if ((extension_word_i >= 16'h0980) && (extension_word_i <= 16'h09ff)) begin // Jcc.EA
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_JCC;
            field_format_id_o = BR_FIELD_FORMAT_F053;
          end
          else if ((extension_word_i >= 16'h0a00) && (extension_word_i <= 16'h0aff)) begin // SETcc.EA
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_SETCC;
            field_format_id_o = BR_FIELD_FORMAT_F052;
          end
          else if ((extension_word_i >= 16'h1000) && (extension_word_i <= 16'h17ff)) begin // MOVcc.A_TO_EA
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_MOVCC;
            field_format_id_o = BR_FIELD_FORMAT_F059;
          end
          else if ((extension_word_i >= 16'h1800) && (extension_word_i <= 16'h1fff)) begin // MOVcc.D_TO_EA
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_MOVCC;
            field_format_id_o = BR_FIELD_FORMAT_F060;
          end
          else if ((extension_word_i >= 16'h2000) && (extension_word_i <= 16'h3fff)) begin // IJcc.D_TO_D_TO_EA
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_IJCC;
            field_format_id_o = BR_FIELD_FORMAT_F064;
          end
          else if ((extension_word_i >= 16'h4000) && (extension_word_i <= 16'h47ff)) begin // MOVcc.EA_TO_A
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_MOVCC;
            field_format_id_o = BR_FIELD_FORMAT_F059;
          end
          else if ((extension_word_i >= 16'h4800) && (extension_word_i <= 16'h4fff)) begin // MOVcc.EA_TO_D
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_MOVCC;
            field_format_id_o = BR_FIELD_FORMAT_F060;
          end
          else if ((extension_word_i >= 16'h5000) && (extension_word_i <= 16'h57ff)) begin // FMOVcc.EA_TO_F
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_FMOVCC;
            field_format_id_o = BR_FIELD_FORMAT_F061;
          end
          else if ((extension_word_i >= 16'h5800) && (extension_word_i <= 16'h5fff)) begin // FMOVcc.F_TO_EA
            valid_o = 1'b1;
            opcode_id_o = BR_OPCODE_FMOVCC;
            field_format_id_o = BR_FIELD_FORMAT_F061;
          end
        end
        BR_EXT_ROOT_CONTROL_FLOW: begin // EXT.control_flow
          casez (extension_word_i)
            16'b0000_0000_00??_????: begin // CALL.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CALL;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            16'b0000_0000_0100_0000: begin // LRET
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_LRET;
              field_format_id_o = BR_FIELD_FORMAT_NONE;
            end
            16'b0000_001?_????_????: begin // LCALL.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_LCALL;
              field_format_id_o = BR_FIELD_FORMAT_F023;
            end
            16'b0000_010?_????_????: begin // LJMP.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_LJMP;
              field_format_id_o = BR_FIELD_FORMAT_F023;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_DATA_MOVEMENT: begin // EXT.data_movement
          casez (extension_word_i)
            16'b0000_0???_????_????: begin // MOV.D_TO_EA_WIDE
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MOV;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_1???_????_????: begin // MOV.EA_TO_D_WIDE
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MOV;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0001_0???_????_????: begin // XCHG.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_XCHG;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0001_1???_????_????: begin // XCHG.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_XCHG;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b01??_????_????_????: begin // MOV.EA_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MOV;
              field_format_id_o = BR_FIELD_FORMAT_F048;
              repg_fast_candidate_o = 1'b1;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_DATA_REGISTER_BANKING: begin // EXT.data_register_banking
          casez (extension_word_i)
            16'b0000_0000_0000_0???: begin // GETDB.D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_GETDB;
              field_format_id_o = BR_FIELD_FORMAT_F004;
            end
            16'b0000_0000_0000_1???: begin // SELDB.D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SELDB;
              field_format_id_o = BR_FIELD_FORMAT_F004;
            end
            16'b0000_0000_0001_????: begin // MOVSETAD.DB_TO_BITMAP
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MOVSETAD;
              field_format_id_o = BR_FIELD_FORMAT_F011;
            end
            16'b0000_0000_0010_????: begin // MOVSETDA.DB_TO_BITMAP
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MOVSETDA;
              field_format_id_o = BR_FIELD_FORMAT_F011;
            end
            16'b0000_0000_0011_????: begin // SELDB.DB
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SELDB;
              field_format_id_o = BR_FIELD_FORMAT_F002;
            end
            16'b0000_0000_0100_????: begin // XCHGSETAD.DB_TO_BITMAP
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_XCHGSETAD;
              field_format_id_o = BR_FIELD_FORMAT_F011;
            end
            16'b0000_0000_0101_????: begin // XCHGSETDA.DB_TO_BITMAP
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_XCHGSETDA;
              field_format_id_o = BR_FIELD_FORMAT_F011;
            end
            16'b0000_0001_????_????: begin // MOVSETDD.DB_TO_DB_TO_BITMAP
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MOVSETDD;
              field_format_id_o = BR_FIELD_FORMAT_F033;
            end
            16'b0000_0010_????_????: begin // XCHGSETDD.DB_TO_DB_TO_BITMAP
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_XCHGSETDD;
              field_format_id_o = BR_FIELD_FORMAT_F033;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_EA_UTILITY: begin // EXT.ea_utility
          casez (extension_word_i)
            16'b0000_000?_????_????: begin // LEA.EA_TO_A
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_LEA;
              field_format_id_o = BR_FIELD_FORMAT_F021;
            end
            16'b0000_001?_????_????: begin // SEGLEA.EA_TO_A
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SEGLEA;
              field_format_id_o = BR_FIELD_FORMAT_F021;
            end
            16'b0000_0100_00??_????: begin // TESTCANON.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_TESTCANON;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_FPU_ARITHMETIC: begin // EXT.fpu_arithmetic
          casez (extension_word_i)
            16'b0000_000?_????_????: begin // FABS.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FABS;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0000_001?_????_????: begin // FADD.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FADD;
              field_format_id_o = BR_FIELD_FORMAT_F051;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0100_0000_0000: begin // FBNDII.F_TO_EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FBNDII;
              field_format_id_o = BR_FIELD_FORMAT_F057;
            end
            16'b0000_0100_0000_0001: begin // FBNDII.F_TO_F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FBNDII;
              field_format_id_o = BR_FIELD_FORMAT_F058;
            end
            16'b0000_0100_0000_0010: begin // FBNDIX.F_TO_EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FBNDIX;
              field_format_id_o = BR_FIELD_FORMAT_F057;
            end
            16'b0000_0100_0000_0011: begin // FBNDIX.F_TO_F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FBNDIX;
              field_format_id_o = BR_FIELD_FORMAT_F058;
            end
            16'b0000_0100_0000_0100: begin // FBNDXI.F_TO_EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FBNDXI;
              field_format_id_o = BR_FIELD_FORMAT_F057;
            end
            16'b0000_0100_0000_0101: begin // FBNDXI.F_TO_F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FBNDXI;
              field_format_id_o = BR_FIELD_FORMAT_F058;
            end
            16'b0000_0100_0000_0110: begin // FBNDXX.F_TO_EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FBNDXX;
              field_format_id_o = BR_FIELD_FORMAT_F057;
            end
            16'b0000_0100_0000_0111: begin // FBNDXX.F_TO_F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FBNDXX;
              field_format_id_o = BR_FIELD_FORMAT_F058;
            end
            16'b0000_0100_0000_1000: begin // FCOPYSIGN.F_TO_F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCOPYSIGN;
              field_format_id_o = BR_FIELD_FORMAT_F058;
            end
            16'b0000_0100_0000_1001: begin // FMADD.EA_TO_F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMADD;
              field_format_id_o = BR_FIELD_FORMAT_F057;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0100_0000_1010: begin // FMADD.F_TO_EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMADD;
              field_format_id_o = BR_FIELD_FORMAT_F057;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0100_0000_1011: begin // FMADD.F_TO_F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMADD;
              field_format_id_o = BR_FIELD_FORMAT_F058;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0100_0000_1100: begin // FMSUB.EA_TO_F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMSUB;
              field_format_id_o = BR_FIELD_FORMAT_F057;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0100_0000_1101: begin // FMSUB.F_TO_EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMSUB;
              field_format_id_o = BR_FIELD_FORMAT_F057;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0100_0000_1110: begin // FMSUB.F_TO_F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMSUB;
              field_format_id_o = BR_FIELD_FORMAT_F058;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0100_0000_1111: begin // FNMADD.EA_TO_F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FNMADD;
              field_format_id_o = BR_FIELD_FORMAT_F057;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0100_0001_????: begin // FCLR.F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCLR;
              field_format_id_o = BR_FIELD_FORMAT_F006;
            end
            16'b0000_0100_0010_0000: begin // FNMADD.F_TO_EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FNMADD;
              field_format_id_o = BR_FIELD_FORMAT_F057;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0100_0010_0001: begin // FNMADD.F_TO_F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FNMADD;
              field_format_id_o = BR_FIELD_FORMAT_F058;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0100_0010_0010: begin // FNMSUB.EA_TO_F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FNMSUB;
              field_format_id_o = BR_FIELD_FORMAT_F057;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0100_0010_0011: begin // FNMSUB.F_TO_EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FNMSUB;
              field_format_id_o = BR_FIELD_FORMAT_F057;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0100_0010_0100: begin // FNMSUB.F_TO_F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FNMSUB;
              field_format_id_o = BR_FIELD_FORMAT_F058;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0100_0010_0101: begin // FPOPM.BITMAP
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FPOPM;
              field_format_id_o = BR_FIELD_FORMAT_F010;
            end
            16'b0000_0100_0010_0110: begin // FPUSHM.BITMAP
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FPUSHM;
              field_format_id_o = BR_FIELD_FORMAT_F010;
            end
            16'b0000_0100_01??_????: begin // FCLR.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCLR;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            16'b0000_0101_????_????: begin // FXCHG.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FXCHG;
              field_format_id_o = BR_FIELD_FORMAT_F026;
            end
            16'b0000_011?_????_????: begin // FCEIL.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCEIL;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0000_1???_????_????: begin // FCEIL.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCEIL;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b0001_0???_????_????: begin // FCEIL.F_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCEIL;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b0001_1???_????_????: begin // FDIV.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FDIV;
              field_format_id_o = BR_FIELD_FORMAT_F049;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0010_000?_????_????: begin // FDIV.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FDIV;
              field_format_id_o = BR_FIELD_FORMAT_F051;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0010_001?_????_????: begin // FFLOOR.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FFLOOR;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0010_010?_????_????: begin // FGETEXP.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FGETEXP;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0010_011?_????_????: begin // FGETMAN.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FGETMAN;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0010_1???_????_????: begin // FFLOOR.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FFLOOR;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b0011_0???_????_????: begin // FFLOOR.F_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FFLOOR;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b0011_1???_????_????: begin // FGETEXP.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FGETEXP;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b0100_0???_????_????: begin // FGETMAN.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FGETMAN;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b0100_1???_????_????: begin // FINT.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FINT;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b0101_0???_????_????: begin // FINT.F_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FINT;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b0101_100?_????_????: begin // FINT.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FINT;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0101_101?_????_????: begin // FINTRZ.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FINTRZ;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0101_110?_????_????: begin // FMAX.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMAX;
              field_format_id_o = BR_FIELD_FORMAT_F051;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0101_111?_????_????: begin // FMIN.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMIN;
              field_format_id_o = BR_FIELD_FORMAT_F051;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0110_0???_????_????: begin // FINTRZ.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FINTRZ;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b0110_1???_????_????: begin // FINTRZ.F_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FINTRZ;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b0111_0???_????_????: begin // FMAX.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMAX;
              field_format_id_o = BR_FIELD_FORMAT_F049;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0111_1???_????_????: begin // FMIN.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMIN;
              field_format_id_o = BR_FIELD_FORMAT_F049;
              repg_fast_candidate_o = 1'b1;
            end
            16'b1000_0???_????_????: begin // FMOD.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMOD;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b1000_100?_????_????: begin // FMOD.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMOD;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b1000_101?_????_????: begin // FMUL.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMUL;
              field_format_id_o = BR_FIELD_FORMAT_F051;
              repg_fast_candidate_o = 1'b1;
            end
            16'b1000_110?_????_????: begin // FNEG.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FNEG;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b1000_111?_????_????: begin // FREM.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FREM;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b1001_0???_????_????: begin // FMUL.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMUL;
              field_format_id_o = BR_FIELD_FORMAT_F049;
              repg_fast_candidate_o = 1'b1;
            end
            16'b1001_1???_????_????: begin // FNEG.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FNEG;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b1010_0???_????_????: begin // FNEG.F_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FNEG;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b1010_1???_????_????: begin // FREM.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FREM;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b1011_0???_????_????: begin // FROUND.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FROUND;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b1011_1???_????_????: begin // FROUND.F_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FROUND;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b1100_000?_????_????: begin // FROUND.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FROUND;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b1100_001?_????_????: begin // FSCALE.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FSCALE;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b1100_010?_????_????: begin // FSQRT.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FSQRT;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b1100_011?_????_????: begin // FSUB.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FSUB;
              field_format_id_o = BR_FIELD_FORMAT_F051;
              repg_fast_candidate_o = 1'b1;
            end
            16'b1100_1???_????_????: begin // FSCALE.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FSCALE;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b1101_0???_????_????: begin // FSQRT.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FSQRT;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b1101_1???_????_????: begin // FSQRT.F_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FSQRT;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b1110_0???_????_????: begin // FSUB.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FSUB;
              field_format_id_o = BR_FIELD_FORMAT_F049;
              repg_fast_candidate_o = 1'b1;
            end
            16'b1110_1???_????_????: begin // FTRUNC.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FTRUNC;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b1111_0???_????_????: begin // FTRUNC.F_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FTRUNC;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b1111_100?_????_????: begin // FTRUNC.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FTRUNC;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_FPU_ARITHMETIC_EA_WIDE: begin // EXT.fpu_arithmetic_ea_wide
          casez (extension_word_i)
            16'b0000_0???_????_????: begin // FABS.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FABS;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b0000_1???_????_????: begin // FABS.F_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FABS;
              field_format_id_o = BR_FIELD_FORMAT_F049;
            end
            16'b0001_0???_????_????: begin // FADD.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FADD;
              field_format_id_o = BR_FIELD_FORMAT_F049;
              repg_fast_candidate_o = 1'b1;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_FPU_MOVE_COMPARE: begin // EXT.fpu_move_compare
          casez (extension_word_i)
            16'b0000_000?_????_????: begin // FCMP.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCMP;
              field_format_id_o = BR_FIELD_FORMAT_F051;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0010_000?_????: begin // FTEST.F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FTEST;
              field_format_id_o = BR_FIELD_FORMAT_F028;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0010_0010_????: begin // FMOVCR.IMM_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMOVCR;
              field_format_id_o = BR_FIELD_FORMAT_F027;
            end
            16'b0000_0010_1???_????: begin // FCVT.D_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCVT;
              field_format_id_o = BR_FIELD_FORMAT_F018;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0011_????_????: begin // FCLASS.F_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCLASS;
              field_format_id_o = BR_FIELD_FORMAT_F040;
            end
            16'b0000_010?_????_????: begin // FMOV.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMOV;
              field_format_id_o = BR_FIELD_FORMAT_F051;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0110_0???_????: begin // FCVT.F_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCVT;
              field_format_id_o = BR_FIELD_FORMAT_F018;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0110_1???_????: begin // FCVTU.D_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCVTU;
              field_format_id_o = BR_FIELD_FORMAT_F018;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0111_????_????: begin // FCVT.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCVT;
              field_format_id_o = BR_FIELD_FORMAT_F026;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_1???_????_????: begin // FCMP.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCMP;
              field_format_id_o = BR_FIELD_FORMAT_F049;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0001_0000_0???_????: begin // FTEST.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FTEST;
              field_format_id_o = BR_FIELD_FORMAT_F025;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0001_0000_1???_????: begin // FCVTU.F_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCVTU;
              field_format_id_o = BR_FIELD_FORMAT_F018;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0001_0001_????_????: begin // FCVTU.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCVTU;
              field_format_id_o = BR_FIELD_FORMAT_F026;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0001_1???_????_????: begin // FMOV.EA_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMOV;
              field_format_id_o = BR_FIELD_FORMAT_F049;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0010_0???_????_????: begin // FMOV.F_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FMOV;
              field_format_id_o = BR_FIELD_FORMAT_F049;
              repg_fast_candidate_o = 1'b1;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_FPU_TRANSCENDENTAL: begin // EXT.fpu_transcendental
          casez (extension_word_i)
            16'b0000_000?_????_????: begin // FACOS.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FACOS;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0000_001?_????_????: begin // FASIN.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FASIN;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0000_010?_????_????: begin // FATAN.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FATAN;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0000_011?_????_????: begin // FATANH.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FATANH;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0000_100?_????_????: begin // FCOS.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCOS;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0000_101?_????_????: begin // FCOSH.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FCOSH;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0000_110?_????_????: begin // FETOX.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FETOX;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0000_111?_????_????: begin // FETOXM1.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FETOXM1;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0001_000?_????_????: begin // FLOG10.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FLOG10;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0001_001?_????_????: begin // FLOG2.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FLOG2;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0001_010?_????_????: begin // FLOGN.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FLOGN;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0001_011?_????_????: begin // FLOGNP1.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FLOGNP1;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0001_100?_????_????: begin // FSIN.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FSIN;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0001_101?_????_????: begin // FSINCOS.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FSINCOS;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0001_110?_????_????: begin // FSINH.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FSINH;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0001_111?_????_????: begin // FTAN.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FTAN;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0010_000?_????_????: begin // FTANH.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FTANH;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0010_001?_????_????: begin // FTENTOX.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FTENTOX;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            16'b0010_010?_????_????: begin // FTWOTOX.F_TO_F
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FTWOTOX;
              field_format_id_o = BR_FIELD_FORMAT_F051;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_ALU: begin // EXT.integer_alu
          casez (extension_word_i)
            16'b0000_0000_????_????: begin // ABS.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ABS;
              field_format_id_o = BR_FIELD_FORMAT_F022;
            end
            16'b0000_0001_00??_????: begin // CLR.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CLR;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            16'b0000_0001_010?_????: begin // SUM.BITMAP_TO_A
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SUM;
              field_format_id_o = BR_FIELD_FORMAT_F032;
            end
            16'b0000_0001_011?_????: begin // SUM.BITMAP_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SUM;
              field_format_id_o = BR_FIELD_FORMAT_F037;
            end
            16'b0000_0001_1???_????: begin // EXTSL.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTSL;
              field_format_id_o = BR_FIELD_FORMAT_F038;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_001?_????_????: begin // ADD.EA_TO_A
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ADD;
              field_format_id_o = BR_FIELD_FORMAT_F021;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_010?_????_????: begin // CMP.EA_TO_A
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CMP;
              field_format_id_o = BR_FIELD_FORMAT_F021;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0000_0110_????_????: begin // DEC.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_DEC;
              field_format_id_o = BR_FIELD_FORMAT_F022;
            end
            16'b0000_0111_????_????: begin // DECN.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_DECN;
              field_format_id_o = BR_FIELD_FORMAT_F022;
            end
            16'b0000_1???_????_????: begin // AND.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_AND;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0001_0???_????_????: begin // CMP.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CMP;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0001_1???_????_????: begin // CMP.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CMP;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0010_00??_????_????: begin // EXTSL.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTSL;
              field_format_id_o = BR_FIELD_FORMAT_F043;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0010_01??_????_????: begin // EXTSL.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTSL;
              field_format_id_o = BR_FIELD_FORMAT_F043;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0010_1???_????_????: begin // EXTSQ.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTSQ;
              field_format_id_o = BR_FIELD_FORMAT_F044;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0011_0???_????_????: begin // EXTSQ.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTSQ;
              field_format_id_o = BR_FIELD_FORMAT_F044;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0011_100?_????_????: begin // EXTSW.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTSW;
              field_format_id_o = BR_FIELD_FORMAT_F023;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0011_101?_????_????: begin // EXTSW.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTSW;
              field_format_id_o = BR_FIELD_FORMAT_F023;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0011_11??_????_????: begin // EXTZL.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTZL;
              field_format_id_o = BR_FIELD_FORMAT_F043;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0100_00??_????_????: begin // EXTZL.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTZL;
              field_format_id_o = BR_FIELD_FORMAT_F043;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0100_0100_????_????: begin // INC.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_INC;
              field_format_id_o = BR_FIELD_FORMAT_F022;
            end
            16'b0100_0101_????_????: begin // INCN.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_INCN;
              field_format_id_o = BR_FIELD_FORMAT_F022;
            end
            16'b0100_0110_????_????: begin // NEG.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_NEG;
              field_format_id_o = BR_FIELD_FORMAT_F022;
            end
            16'b0100_0111_????_????: begin // NOT.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_NOT;
              field_format_id_o = BR_FIELD_FORMAT_F022;
            end
            16'b0100_1???_????_????: begin // EXTZQ.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTZQ;
              field_format_id_o = BR_FIELD_FORMAT_F044;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0101_0???_????_????: begin // EXTZQ.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTZQ;
              field_format_id_o = BR_FIELD_FORMAT_F044;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0101_1???_????_????: begin // MAXS.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MAXS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0110_0???_????_????: begin // MAXS.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MAXS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0110_1???_????_????: begin // MAXU.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MAXU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0111_0???_????_????: begin // MAXU.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MAXU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0111_1???_????_????: begin // MINS.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MINS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1000_0???_????_????: begin // MINS.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MINS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1000_1???_????_????: begin // MINU.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MINU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1001_0???_????_????: begin // MINU.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MINU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1001_1???_????_????: begin // OR.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_OR;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b1010_0???_????_????: begin // OR.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_OR;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b1010_1000_????_????: begin // REVBYTE.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_REVBYTE;
              field_format_id_o = BR_FIELD_FORMAT_F039;
            end
            16'b1010_101?_????_????: begin // SUB.EA_TO_A
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SUB;
              field_format_id_o = BR_FIELD_FORMAT_F021;
              repg_fast_candidate_o = 1'b1;
            end
            16'b1011_0???_????_????: begin // REVBYTE.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_REVBYTE;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1011_1???_????_????: begin // REVBYTE.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_REVBYTE;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1100_0???_????_????: begin // SBB.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SBB;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1100_1???_????_????: begin // SBB.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SBB;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1101_0???_????_????: begin // SUB.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SUB;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b1101_1???_????_????: begin // SUB.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SUB;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b1110_0???_????_????: begin // TEST.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_TEST;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b1110_1???_????_????: begin // TEST.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_TEST;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b1111_0???_????_????: begin // XOR.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_XOR;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b1111_1???_????_????: begin // XOR.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_XOR;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_ALU_CMP_EA_WIDE: begin // EXT.integer_alu_cmp_ea_wide
          casez (extension_word_i)
            16'b00??_????_????_????: begin // CMP.EA_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CMP;
              field_format_id_o = BR_FIELD_FORMAT_F048;
              repg_fast_candidate_o = 1'b1;
            end
            16'b01??_????_????_????: begin // CMP.IMM_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CMP;
              field_format_id_o = BR_FIELD_FORMAT_F042;
              repg_fast_candidate_o = 1'b1;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_ALU_IMM_EA_ARITH_WIDE: begin // EXT.integer_alu_imm_ea_arith_wide
          casez (extension_word_i)
            16'b00??_????_????_????: begin // ADC.IMM_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ADC;
              field_format_id_o = BR_FIELD_FORMAT_F042;
            end
            16'b01??_????_????_????: begin // ADD.IMM_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ADD;
              field_format_id_o = BR_FIELD_FORMAT_F042;
              repg_fast_candidate_o = 1'b1;
            end
            16'b10??_????_????_????: begin // SBB.IMM_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SBB;
              field_format_id_o = BR_FIELD_FORMAT_F042;
            end
            16'b11??_????_????_????: begin // SUB.IMM_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SUB;
              field_format_id_o = BR_FIELD_FORMAT_F042;
              repg_fast_candidate_o = 1'b1;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_ALU_IMM_EA_LOGIC_WIDE: begin // EXT.integer_alu_imm_ea_logic_wide
          casez (extension_word_i)
            16'b00??_????_????_????: begin // AND.IMM_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_AND;
              field_format_id_o = BR_FIELD_FORMAT_F042;
              repg_fast_candidate_o = 1'b1;
            end
            16'b01??_????_????_????: begin // OR.IMM_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_OR;
              field_format_id_o = BR_FIELD_FORMAT_F042;
              repg_fast_candidate_o = 1'b1;
            end
            16'b10??_????_????_????: begin // TEST.IMM_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_TEST;
              field_format_id_o = BR_FIELD_FORMAT_F042;
              repg_fast_candidate_o = 1'b1;
            end
            16'b11??_????_????_????: begin // XOR.IMM_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_XOR;
              field_format_id_o = BR_FIELD_FORMAT_F042;
              repg_fast_candidate_o = 1'b1;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_ALU_REG_EA_WIDE: begin // EXT.integer_alu_reg_ea_wide
          casez (extension_word_i)
            16'b0000_0???_????_????: begin // ADC.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ADC;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0000_1???_????_????: begin // ADC.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ADC;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0001_0???_????_????: begin // ADD.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ADD;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0001_1???_????_????: begin // ADD.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ADD;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0010_0???_????_????: begin // AND.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_AND;
              field_format_id_o = BR_FIELD_FORMAT_F045;
              repg_fast_candidate_o = 1'b1;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_BITFIELD: begin // EXT.integer_bitfield
          casez (extension_word_i)
            16'b0000_0000_????_????: begin // BCHG.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BCHG;
              field_format_id_o = BR_FIELD_FORMAT_F039;
            end
            16'b0000_0001_????_????: begin // BCLR.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BCLR;
              field_format_id_o = BR_FIELD_FORMAT_F039;
            end
            16'b0000_0010_????_????: begin // BSET.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BSET;
              field_format_id_o = BR_FIELD_FORMAT_F039;
            end
            16'b0000_0011_????_????: begin // BTEST.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BTEST;
              field_format_id_o = BR_FIELD_FORMAT_F039;
            end
            16'b0000_0100_????_????: begin // PARITY.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_PARITY;
              field_format_id_o = BR_FIELD_FORMAT_F022;
            end
            16'b0000_0101_????_????: begin // RCL.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RCL;
              field_format_id_o = BR_FIELD_FORMAT_F039;
            end
            16'b0000_0110_????_????: begin // RCR.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RCR;
              field_format_id_o = BR_FIELD_FORMAT_F039;
            end
            16'b0000_0111_????_????: begin // REVBIT.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_REVBIT;
              field_format_id_o = BR_FIELD_FORMAT_F039;
            end
            16'b0000_1???_????_????: begin // BCHG.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BCHG;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0001_0???_????_????: begin // BCLR.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BCLR;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0001_1???_????_????: begin // BSET.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BSET;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0010_0???_????_????: begin // BTEST.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BTEST;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0010_1???_????_????: begin // CLS.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CLS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0011_0???_????_????: begin // CLZ.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CLZ;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0011_1???_????_????: begin // CTS.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CTS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0100_0???_????_????: begin // CTZ.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CTZ;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0100_1???_????_????: begin // POPCNT.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_POPCNT;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0101_0???_????_????: begin // RCL.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RCL;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0101_1???_????_????: begin // RCR.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RCR;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0110_0???_????_????: begin // REVBIT.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_REVBIT;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0110_1???_????_????: begin // REVBIT.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_REVBIT;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0111_0000_????_????: begin // ROL.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ROL;
              field_format_id_o = BR_FIELD_FORMAT_F039;
            end
            16'b0111_0001_????_????: begin // ROR.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ROR;
              field_format_id_o = BR_FIELD_FORMAT_F039;
            end
            16'b0111_0010_????_????: begin // SAR.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SAR;
              field_format_id_o = BR_FIELD_FORMAT_F039;
            end
            16'b0111_0011_????_????: begin // SHL.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SHL;
              field_format_id_o = BR_FIELD_FORMAT_F039;
            end
            16'b0111_0100_????_????: begin // SHR.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SHR;
              field_format_id_o = BR_FIELD_FORMAT_F039;
            end
            16'b0111_1???_????_????: begin // ROL.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ROL;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1000_0???_????_????: begin // ROR.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ROR;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1000_1???_????_????: begin // SAR.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SAR;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1001_0???_????_????: begin // SHL.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SHL;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1001_1???_????_????: begin // SHR.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SHR;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_BITFIELD_BIT_IMM: begin // EXT.integer_bitfield_bit_imm
          casez (extension_word_i)
            16'b00??_????_????_????: begin // BCHG.I6_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BCHG;
              field_format_id_o = BR_FIELD_FORMAT_F050;
            end
            16'b01??_????_????_????: begin // BCLR.I6_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BCLR;
              field_format_id_o = BR_FIELD_FORMAT_F050;
            end
            16'b10??_????_????_????: begin // BSET.I6_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BSET;
              field_format_id_o = BR_FIELD_FORMAT_F050;
            end
            16'b11??_????_????_????: begin // BTEST.I6_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BTEST;
              field_format_id_o = BR_FIELD_FORMAT_F050;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_BITFIELD_ROTATE_IMM: begin // EXT.integer_bitfield_rotate_imm
          casez (extension_word_i)
            16'b00??_????_????_????: begin // RCL.I6_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RCL;
              field_format_id_o = BR_FIELD_FORMAT_F050;
            end
            16'b01??_????_????_????: begin // RCR.I6_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RCR;
              field_format_id_o = BR_FIELD_FORMAT_F050;
            end
            16'b10??_????_????_????: begin // ROL.I6_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ROL;
              field_format_id_o = BR_FIELD_FORMAT_F050;
            end
            16'b11??_????_????_????: begin // ROR.I6_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ROR;
              field_format_id_o = BR_FIELD_FORMAT_F050;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_BITFIELD_SHIFT_IMM: begin // EXT.integer_bitfield_shift_imm
          casez (extension_word_i)
            16'b00??_????_????_????: begin // SHL.I6_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SHL;
              field_format_id_o = BR_FIELD_FORMAT_F050;
            end
            16'b01??_????_????_????: begin // SHR.I6_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SHR;
              field_format_id_o = BR_FIELD_FORMAT_F050;
            end
            16'b10??_????_????_????: begin // SAR.I6_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SAR;
              field_format_id_o = BR_FIELD_FORMAT_F050;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_BOUNDS_SIGNED: begin // EXT.integer_bounds_signed
          casez (extension_word_i)
            16'b00??_????_????_????: begin // BNDSII.D_TO_EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BNDSII;
              field_format_id_o = BR_FIELD_FORMAT_F055;
            end
            16'b01??_????_????_????: begin // BNDSIX.D_TO_EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BNDSIX;
              field_format_id_o = BR_FIELD_FORMAT_F055;
            end
            16'b10??_????_????_????: begin // BNDSXI.D_TO_EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BNDSXI;
              field_format_id_o = BR_FIELD_FORMAT_F055;
            end
            16'b11??_????_????_????: begin // BNDSXX.D_TO_EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BNDSXX;
              field_format_id_o = BR_FIELD_FORMAT_F055;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_BOUNDS_UNSIGNED: begin // EXT.integer_bounds_unsigned
          casez (extension_word_i)
            16'b00??_????_????_????: begin // BNDUII.D_TO_EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BNDUII;
              field_format_id_o = BR_FIELD_FORMAT_F055;
            end
            16'b01??_????_????_????: begin // BNDUIX.D_TO_EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BNDUIX;
              field_format_id_o = BR_FIELD_FORMAT_F055;
            end
            16'b10??_????_????_????: begin // BNDUXI.D_TO_EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BNDUXI;
              field_format_id_o = BR_FIELD_FORMAT_F055;
            end
            16'b11??_????_????_????: begin // BNDUXX.D_TO_EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_BNDUXX;
              field_format_id_o = BR_FIELD_FORMAT_F055;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_EXTEND_EA_WIDE: begin // EXT.integer_extend_ea_wide
          casez (extension_word_i)
            16'b000?_????_????_????: begin // EXTSL.EA_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTSL;
              field_format_id_o = BR_FIELD_FORMAT_F046;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0010_????_????_????: begin // EXTSW.EA_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTSW;
              field_format_id_o = BR_FIELD_FORMAT_F024;
              repg_fast_candidate_o = 1'b1;
            end
            16'b0011_????_????_????: begin // EXTZW.EA_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTZW;
              field_format_id_o = BR_FIELD_FORMAT_F024;
              repg_fast_candidate_o = 1'b1;
            end
            16'b01??_????_????_????: begin // EXTSQ.EA_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTSQ;
              field_format_id_o = BR_FIELD_FORMAT_F047;
              repg_fast_candidate_o = 1'b1;
            end
            16'b100?_????_????_????: begin // EXTZL.EA_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTZL;
              field_format_id_o = BR_FIELD_FORMAT_F046;
              repg_fast_candidate_o = 1'b1;
            end
            16'b11??_????_????_????: begin // EXTZQ.EA_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_EXTZQ;
              field_format_id_o = BR_FIELD_FORMAT_F047;
              repg_fast_candidate_o = 1'b1;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_MAC: begin // EXT.integer_mac
          casez (extension_word_i)
            16'b00??_????_????_????: begin // MADD.EA_TO_D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MADD;
              field_format_id_o = BR_FIELD_FORMAT_F055;
            end
            16'b01??_????_????_????: begin // MSUB.EA_TO_D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MSUB;
              field_format_id_o = BR_FIELD_FORMAT_F055;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_INTEGER_MUL_DIV: begin // EXT.integer_mul_div
          casez (extension_word_i)
            16'b0000_0???_????_????: begin // CLMUL.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CLMUL;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0000_1???_????_????: begin // CLMUL.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CLMUL;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0001_0???_????_????: begin // CLMULH.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CLMULH;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0001_1???_????_????: begin // CLMULH.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CLMULH;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0010_0000_0000_0000: begin // DIVMODS.EA_TO_D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_DIVMODS;
              field_format_id_o = BR_FIELD_FORMAT_F056;
            end
            16'b0010_1???_????_????: begin // DIVS.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_DIVS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0011_0???_????_????: begin // DIVS.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_DIVS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b0011_1???_????_????: begin // DIVU.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_DIVU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b01??_????_????_????: begin // DIVMODU.EA_TO_D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_DIVMODU;
              field_format_id_o = BR_FIELD_FORMAT_F055;
            end
            16'b1000_0???_????_????: begin // DIVU.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_DIVU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1000_1???_????_????: begin // MODS.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MODS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1001_0???_????_????: begin // MODS.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MODS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1001_1???_????_????: begin // MODU.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MODU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1010_0???_????_????: begin // MODU.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MODU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1010_1???_????_????: begin // MULHS.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MULHS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1011_0???_????_????: begin // MULHS.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MULHS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1011_1???_????_????: begin // MULHSU.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MULHSU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1100_0???_????_????: begin // MULHSU.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MULHSU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1100_1???_????_????: begin // MULHU.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MULHU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1101_0???_????_????: begin // MULHU.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MULHU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1101_1???_????_????: begin // MULS.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MULS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1110_0???_????_????: begin // MULS.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MULS;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1110_1???_????_????: begin // MULU.D_TO_EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MULU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            16'b1111_0???_????_????: begin // MULU.EA_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_MULU;
              field_format_id_o = BR_FIELD_FORMAT_F045;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_SYSTEM_CORE: begin // EXT.system_core
          casez (extension_word_i)
            16'b0000_0000_0000_0???: begin // RDCR.D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RDCR;
              field_format_id_o = BR_FIELD_FORMAT_F016;
            end
            16'b0000_0000_0000_1???: begin // WRCR.D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_WRCR;
              field_format_id_o = BR_FIELD_FORMAT_F016;
            end
            16'b0000_0000_0001_0???: begin // RDFLAGS.D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RDFLAGS;
              field_format_id_o = BR_FIELD_FORMAT_F004;
            end
            16'b0000_0000_0001_1???: begin // WRFLAGS.D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_WRFLAGS;
              field_format_id_o = BR_FIELD_FORMAT_F004;
            end
            16'b0000_0000_0010_0???: begin // RDSTATUS.D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RDSTATUS;
              field_format_id_o = BR_FIELD_FORMAT_F004;
            end
            16'b0000_0000_0010_1???: begin // WRSTATUS.D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_WRSTATUS;
              field_format_id_o = BR_FIELD_FORMAT_F004;
            end
            16'b0000_0000_0011_0???: begin // CPUID.D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_CPUID;
              field_format_id_o = BR_FIELD_FORMAT_F004;
            end
            16'b0000_0000_0011_1???: begin // RDFSTATUS.D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RDFSTATUS;
              field_format_id_o = BR_FIELD_FORMAT_F004;
            end
            16'b0000_0000_01??_????: begin // RDSEG.S_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RDSEG;
              field_format_id_o = BR_FIELD_FORMAT_F029;
            end
            16'b0000_0000_10??_????: begin // WRSEG.D_TO_S
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_WRSEG;
              field_format_id_o = BR_FIELD_FORMAT_F020;
            end
            16'b0000_0000_11??_????: begin // SAVE.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SAVE;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            16'b0000_0001_00??_????: begin // RESTORE.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RESTORE;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            16'b0000_0001_0100_0???: begin // RDPMC.IMM_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RDPMC;
              field_format_id_o = BR_FIELD_FORMAT_F019;
            end
            16'b0000_0001_0100_1???: begin // WRFSTATUS.D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_WRFSTATUS;
              field_format_id_o = BR_FIELD_FORMAT_F004;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_TLB_CACHE: begin // EXT.tlb_cache
          casez (extension_word_i)
            16'b0000_0000_0000_0000: begin // INVTLB
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_INVTLB;
              field_format_id_o = BR_FIELD_FORMAT_NONE;
            end
            16'b0000_0000_0000_0001: begin // INVASID.IMM
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_INVASID;
              field_format_id_o = BR_FIELD_FORMAT_F007;
            end
            16'b0000_0000_0000_1???: begin // SWPT.D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SWPT;
              field_format_id_o = BR_FIELD_FORMAT_F004;
            end
            16'b0000_0000_0001_0???: begin // RDPTC.D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_RDPTC;
              field_format_id_o = BR_FIELD_FORMAT_F004;
            end
            16'b0000_0000_01??_????: begin // INVPAGE.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_INVPAGE;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            16'b0000_0000_10??_????: begin // SWPTA.D_TO_D
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SWPTA;
              field_format_id_o = BR_FIELD_FORMAT_F017;
            end
            16'b0000_0000_11??_????: begin // INVDCACHE.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_INVDCACHE;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            16'b0000_0001_00??_????: begin // WRBKDCACHE.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_WRBKDCACHE;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            16'b0000_0001_01??_????: begin // FLSHDCACHE.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_FLSHDCACHE;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            16'b0000_0001_10??_????: begin // INVICACHE.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_INVICACHE;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            16'b0000_0001_11??_????: begin // SYNCCACHE.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_SYNCCACHE;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            16'b0000_0010_00??_????: begin // PTATTR.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_PTATTR;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            16'b0000_0010_01??_????: begin // PTQUERY.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_PTQUERY;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            16'b0000_0010_10??_????: begin // VTOP.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_VTOP;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            default: begin
            end
          endcase
        end
        BR_EXT_ROOT_VIRTUALIZATION_ACCELERATION: begin // EXT.virtualization_acceleration
          casez (extension_word_i)
            16'b0000_0000_00??_????: begin // ENCINST.EA
              valid_o = 1'b1;
              opcode_id_o = BR_OPCODE_ENCINST;
              field_format_id_o = BR_FIELD_FORMAT_F005;
            end
            default: begin
            end
          endcase
        end
        default: begin
        end
      endcase
    end

    if (valid_o) begin
      case (field_format_id_o)
        BR_FIELD_FORMAT_F002: field_format_token_words = 4'd2; // DBANK4@1:0
        BR_FIELD_FORMAT_F004: field_format_token_words = 4'd2; // DREG3@1:0
        BR_FIELD_FORMAT_F005: field_format_token_words = 4'd2; // EA6@1:0
        BR_FIELD_FORMAT_F006: field_format_token_words = 4'd2; // FREG4@1:0
        BR_FIELD_FORMAT_F007: field_format_token_words = 4'd3; // IMM1616@2:0
        BR_FIELD_FORMAT_F010: field_format_token_words = 4'd3; // fbitmap1616@2:0
        BR_FIELD_FORMAT_F011: field_format_token_words = 4'd3; // DBANK4@1:0_bitmap1616@2:0
        BR_FIELD_FORMAT_F016: field_format_token_words = 4'd3; // DREG3@1:0_CR16@2:0
        BR_FIELD_FORMAT_F017: field_format_token_words = 4'd2; // DREG3@1:0_DREG3@1:3
        BR_FIELD_FORMAT_F018: field_format_token_words = 4'd2; // DREG3@1:0_FREG4@1:3
        BR_FIELD_FORMAT_F019: field_format_token_words = 4'd3; // DREG3@1:0_IMM1616@2:0
        BR_FIELD_FORMAT_F020: field_format_token_words = 4'd2; // DREG3@1:0_SREG3@1:3
        BR_FIELD_FORMAT_F021: field_format_token_words = 4'd2; // EA6@1:0_AREG3@1:6
        BR_FIELD_FORMAT_F022: field_format_token_words = 4'd2; // EA6@1:0_BWLQ2@1:6
        BR_FIELD_FORMAT_F023: field_format_token_words = 4'd2; // EA6@1:0_DREG3@1:6
        BR_FIELD_FORMAT_F024: field_format_token_words = 4'd2; // EA6@1:0_EA6@1:6
        BR_FIELD_FORMAT_F025: field_format_token_words = 4'd2; // EA6@1:0_S_D1@1:6
        BR_FIELD_FORMAT_F026: field_format_token_words = 4'd2; // FREG4@1:0_FREG4@1:4
        BR_FIELD_FORMAT_F027: field_format_token_words = 4'd3; // FREG4@1:0_IMM1616@2:0
        BR_FIELD_FORMAT_F028: field_format_token_words = 4'd2; // FREG4@1:0_S_D1@1:4
        BR_FIELD_FORMAT_F029: field_format_token_words = 4'd2; // SREG3@1:0_DREG3@1:3
        BR_FIELD_FORMAT_F030: field_format_token_words = 4'd2; // WL1@1:0_EA6@1:1
        BR_FIELD_FORMAT_F032: field_format_token_words = 4'd3; // AREG3@1:0_BWLQ2@1:3_bitmap1616@2:0
        BR_FIELD_FORMAT_F033: field_format_token_words = 4'd3; // DBANK4@1:0_DBANK4@1:4_bitmap1616@2:0
        BR_FIELD_FORMAT_F037: field_format_token_words = 4'd3; // DREG3@1:0_BWLQ2@1:3_bitmap1616@2:0
        BR_FIELD_FORMAT_F038: field_format_token_words = 4'd2; // DREG3@1:0_DREG3@1:3_BW1@1:6
        BR_FIELD_FORMAT_F039: field_format_token_words = 4'd2; // DREG3@1:0_DREG3@1:3_BWLQ2@1:6
        BR_FIELD_FORMAT_F040: field_format_token_words = 4'd2; // DREG3@1:0_FREG4@1:3_S_D1@1:7
        BR_FIELD_FORMAT_F042: field_format_token_words = 4'd2; // EA6@1:0_BWLQ2@1:6_IMM66@1:8
        BR_FIELD_FORMAT_F043: field_format_token_words = 4'd2; // EA6@1:0_DREG3@1:6_BW1@1:9
        BR_FIELD_FORMAT_F044: field_format_token_words = 4'd2; // EA6@1:0_DREG3@1:6_BWL2@1:9
        BR_FIELD_FORMAT_F045: field_format_token_words = 4'd2; // EA6@1:0_DREG3@1:6_BWLQ2@1:9
        BR_FIELD_FORMAT_F046: field_format_token_words = 4'd2; // EA6@1:0_EA6@1:6_BW1@1:12
        BR_FIELD_FORMAT_F047: field_format_token_words = 4'd2; // EA6@1:0_EA6@1:6_BWL2@1:12
        BR_FIELD_FORMAT_F048: field_format_token_words = 4'd2; // EA6@1:0_EA6@1:6_BWLQ2@1:12
        BR_FIELD_FORMAT_F049: field_format_token_words = 4'd2; // EA6@1:0_FREG4@1:6_S_D1@1:10
        BR_FIELD_FORMAT_F050: field_format_token_words = 4'd2; // EA6@1:0_selector66@1:6_BWLQ2@1:12
        BR_FIELD_FORMAT_F051: field_format_token_words = 4'd2; // FREG4@1:0_FREG4@1:4_S_D1@1:8
        BR_FIELD_FORMAT_F052: field_format_token_words = 4'd2; // condition4@0:0_EA6@1:0_BWLQ2@1:6
        BR_FIELD_FORMAT_F053: field_format_token_words = 4'd2; // condition4@0:0_EA6@1:0_WL1@1:6
        BR_FIELD_FORMAT_F054: field_format_token_words = 4'd2; // condition4@0:0_FREG4@1:0_FREG4@1:4
        BR_FIELD_FORMAT_F055: field_format_token_words = 4'd2; // EA6@1:0_DREG3@1:6_DREG3@1:9_BWLQ2@1:12
        BR_FIELD_FORMAT_F056: field_format_token_words = 4'd3; // EA6@2:0_DREG3@2:6_DREG3@2:9_BWLQ2@2:12
        BR_FIELD_FORMAT_F057: field_format_token_words = 4'd3; // EA6@2:0_FREG4@2:6_FREG4@2:10_S_D1@2:14
        BR_FIELD_FORMAT_F058: field_format_token_words = 4'd3; // FREG4@2:0_FREG4@2:4_FREG4@2:8_S_D1@2:12
        BR_FIELD_FORMAT_F059: field_format_token_words = 4'd2; // condition4@0:0_EA6@1:0_AREG3@1:6_BWLQ2@1:9
        BR_FIELD_FORMAT_F060: field_format_token_words = 4'd2; // condition4@0:0_EA6@1:0_DREG3@1:6_BWLQ2@1:9
        BR_FIELD_FORMAT_F061: field_format_token_words = 4'd2; // condition4@0:0_EA6@1:0_FREG4@1:6_S_D1@1:10
        BR_FIELD_FORMAT_F062: field_format_token_words = 4'd3; // memory_order3@2:0_EA6@2:3_DREG3@2:9_BWLQ2@2:12
        BR_FIELD_FORMAT_F063: field_format_token_words = 4'd3; // BWLQ2@1:0_memory_order3@2:0_EA6@2:3_DREG3@2:9_DREG3@2:12
        BR_FIELD_FORMAT_F064: field_format_token_words = 4'd2; // condition4@0:0_EA6@1:0_DREG3@1:6_DREG3@1:9_LQ1@1:12
        default: begin
        end
      endcase
      if (field_format_token_words > required_words_o) begin
        required_words_o = field_format_token_words;
      end
    end
  end
endmodule

`default_nettype wire
