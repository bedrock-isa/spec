# Generated Opcode Allocation Plan

Generated from `isa/spec/*.yaml`. Do not edit by hand.

- Solver status: `sat`
- Primary target space: `PRIMARY_PAYLOAD`
- Extended target space: `EXTENDED_OPCODE_WORD`
- Candidates allocated: 383
- One-word compact encodings selected: 60
- Extended encodings selected: 323
- Primary slots used: 3889 / 4096
- Primary free slots: 207
- Primary headroom target: 64
- Natural extension roots: 28
- Extension root primary slots: 43
- Extended opcodes used: 881381 / 1835008
- Allocator compact exclusions: 1
- Allocator compact-policy violations: 0

## Alignment Audit

| Check | Status | Detail |
| --- | --- | --- |
| D register class | `pass` | register class D count=8, width=64 |
| A register class | `pass` | register class A count=8, width=64 |
| REPcc prefix metadata | `pass` | condition field=c, counter field=d, aliases=['REP'] |
| REPG instruction metadata | `pass` | candidates=1, primary_fields=['DREG'], payload_fields=['IMM16'], min_words=2 |
| address-update operand coverage | `pass` | compact update forms=['INDIRECT'], extended update modes=['SEG_A'] |
| EA compact coverage | `pass` | 18 required compact forms covered |
| EA extended coverage | `pass` | 25 required extended forms covered |
| EA operand policy | `pass` | 10 EA sets |
| canonical encoding rules | `pass` | 1 canonical rules |
| fixed primary payloads | `pass` | fixed={'AFENCE': 5, 'HALT': 0, 'ILLEGAL': 4095, 'NOP': 3919, 'WFENCE': 6, 'CALL.IMM16': 3, 'RET': 3888} |
| mandatory compact fit | `pass` | all mandatory compact candidates fit primary payload |
| memory-memory restriction | `pass` | only candidates explicitly marked memory-memory-capable contain two EA operands |
| allocation scope | `info` | 383 candidates allocated together; 95 have one-word field layouts. |

## Decode Cost Audit

| Check | Status | Severity | Detail |
| --- | --- | --- | --- |
| decode_cost_priority_order | `info` | info | aligned_large_ranges > shared_field_layout > family_locality > fewer_singletons > compact_hot_path > visual_symmetry |
| aligned_large_ranges | `fail` | medium | misaligned=['ADD.IMM_TO_D@0x400/961', 'CMP.IMM_TO_D@0x401/961', 'SUB.IMM_TO_D@0x402/961', 'TEST.IMM_TO_D@0x403/961'] |
| extension_roots_high_primary_payload | `pass` | high | min_payload=0xe00, low_roots=none |
| extension_family_root_contiguity | `pass` | medium | extension roots are contiguous within each family |
| compact_singleton_count | `info` | low | 24 one-slot compact patterns after family clustering |

## Field Layout Model

- Field score formula: `candidate_weight_times_field_width`
- Default field score multiplier: `1.0`

| Rank | Signature | Width | Score |
| --- | --- | --- | --- |
| 0 | `COND4` | 4 | 448000 |
| 1 | `EA6` | 6 | 3484440 |
| 2 | `REG3` | 3 | 5950080 |
| 3 | `REG3#2` | 3 | 1474980 |
| 4 | `EA6#2` | 6 | 51000 |
| 5 | `FREG:4` | 4 | 88640 |
| 6 | `FREG:4#2` | 4 | 42240 |
| 7 | `FREG:4#3` | 4 | 5760 |
| 8 | `SEL6` | 6 | 59400 |
| 9 | `DBANK:4` | 4 | 61600 |
| 10 | `DBANK:4#2` | 4 | 17600 |
| 11 | `SIZE2` | 2 | 1133800 |
| 12 | `IMM6:6` | 6 | 48600 |
| 13 | `SIZE1` | 1 | 747680 |

| Container | Subfield | Offset | Score | Examples |
| --- | --- | --- | --- | --- |
| `EA6` | `REG3` | 0 | 1742220 | `MOV.D_TO_EA`, `MOV.EA_TO_D`, `DJcc.D_TO_EA`, `IJcc.D_TO_D_TO_EA` |

| Operand Format | Count | Weight | Examples |
| --- | --- | --- | --- |
| `EA6, REG3, SIZE2` | 86 | 173300 | `DJcc.D_TO_EA`, `MOVcc.D_TO_EA`, `MOVcc.EA_TO_D`, `MOVcc.A_TO_EA` |
| `FREG:4, FREG:4#2, SIZE1` | 41 | 6560 | `FABS.F_TO_F`, `FADD.F_TO_F`, `FCEIL.F_TO_F`, `FCMP.F_TO_F` |
| `EA6, FREG:4, SIZE1` | 34 | 5440 | `FABS.EA_TO_F`, `FABS.F_TO_EA`, `FADD.EA_TO_F`, `FCEIL.EA_TO_F` |
| `REG3` | 22 | 110560 | `CLR.A`, `CLR.D`, `MOV.IMM_TO_A`, `POP.A` |
| `EA6` | 17 | 18820 | `TESTCANON.EA`, `CLR.EA`, `CALL.EA`, `FLSHDCACHE.EA` |
| `REG3, REG3#2, SIZE2` | 15 | 286000 | `EXTSQ.D_TO_D`, `EXTZQ.D_TO_D`, `REVBIT.D_TO_D`, `REVBYTE.D_TO_D` |
| `EA6, REG3, REG3#2, SIZE2` | 13 | 11300 | `BNDSII.D_TO_EA_TO_D`, `BNDSIX.D_TO_EA_TO_D`, `BNDSXI.D_TO_EA_TO_D`, `BNDSXX.D_TO_EA_TO_D` |
| `EA6, FREG:4, FREG:4#2, SIZE1` | 12 | 1920 | `FBNDII.F_TO_EA_TO_F`, `FBNDIX.F_TO_EA_TO_F`, `FBNDXI.F_TO_EA_TO_F`, `FBNDXX.F_TO_EA_TO_F` |
| `EA6, SEL6, SIZE2` | 11 | 9900 | `BCHG.I6_TO_EA`, `BCLR.I6_TO_EA`, `BSET.I6_TO_EA`, `BTEST.I6_TO_EA` |
| `EA6, REG3` | 9 | 50500 | `LCALL.D_TO_EA`, `LJMP.D_TO_EA`, `LEA.EA_TO_A`, `SEGLEA.EA_TO_A` |
| `EA6, SIZE2` | 9 | 21200 | `SETcc.EA`, `ABS.EA`, `DEC.EA`, `DECN.EA` |
| `EA6, SIZE2, IMM6:6` | 9 | 8100 | `ADD.IMM_TO_EA`, `AND.IMM_TO_EA`, `CMP.IMM_TO_EA`, `OR.IMM_TO_EA` |
| `FREG:4, FREG:4#2, FREG:4#3, SIZE1` | 9 | 1440 | `FBNDII.F_TO_F_TO_F`, `FBNDIX.F_TO_F_TO_F`, `FBNDXI.F_TO_F_TO_F`, `FBNDXX.F_TO_F_TO_F` |
| `REG3, REG3#2, SIZE1` | 9 | 162000 | `ADD.D_TO_D`, `AND.D_TO_D`, `CMP.D_TO_D`, `EXTZL.D_TO_D` |
| `REG3, SIZE2` | 9 | 52200 | `ABS.D`, `DEC.D`, `DECN.D`, `INC.D` |
| `REG3, SIZE1` | 7 | 280000 | `ADD.IMM_TO_D`, `AND.IMM_TO_D`, `CMP.IMM_TO_D`, `OR.IMM_TO_D` |

| Similar Formats | Similarity | Shared Placement Pressure | Examples |
| --- | --- | --- | --- |
| `EA6, REG3, SIZE1` / `EA6, REG3, REG3#2, SIZE1` | 0.75 | 10500 | `MOV.D_TO_EA`, `MOV.EA_TO_D`, `IJcc.D_TO_D_TO_EA` |
| `REG3, REG3#2, SIZE1` / `EA6, REG3, REG3#2, SIZE1` | 0.75 | 10500 | `ADD.D_TO_D`, `AND.D_TO_D`, `IJcc.D_TO_D_TO_EA` |
| `EA6, REG3, SIZE2` / `EA6, REG3, REG3#2, SIZE2` | 0.75 | 8475 | `DJcc.D_TO_EA`, `MOVcc.D_TO_EA`, `BNDSII.D_TO_EA_TO_D`, `BNDSIX.D_TO_EA_TO_D` |
| `REG3, REG3#2, SIZE2` / `EA6, REG3, REG3#2, SIZE2` | 0.75 | 8475 | `EXTSQ.D_TO_D`, `EXTZQ.D_TO_D`, `BNDSII.D_TO_EA_TO_D`, `BNDSIX.D_TO_EA_TO_D` |
| `EA6, FREG:4, SIZE1` / `EA6, FREG:4, FREG:4#2, SIZE1` | 0.75 | 1440 | `FABS.EA_TO_F`, `FABS.F_TO_EA`, `FBNDII.F_TO_EA_TO_F`, `FBNDIX.F_TO_EA_TO_F` |
| `FREG:4, FREG:4#2, SIZE1` / `EA6, FREG:4, FREG:4#2, SIZE1` | 0.75 | 1440 | `FABS.F_TO_F`, `FADD.F_TO_F`, `FBNDII.F_TO_EA_TO_F`, `FBNDIX.F_TO_EA_TO_F` |
| `FREG:4, FREG:4#2, SIZE1` / `FREG:4, FREG:4#2, FREG:4#3, SIZE1` | 0.75 | 1080 | `FABS.F_TO_F`, `FADD.F_TO_F`, `FBNDII.F_TO_F_TO_F`, `FBNDIX.F_TO_F_TO_F` |
| `REG3, SIZE1` / `EA6, REG3, SIZE1` | 0.667 | 162400 | `ADD.IMM_TO_D`, `AND.IMM_TO_D`, `MOV.D_TO_EA`, `MOV.EA_TO_D` |
| `REG3, REG3#2, SIZE1` / `REG3, SIZE1` | 0.667 | 108000 | `ADD.D_TO_D`, `AND.D_TO_D`, `ADD.IMM_TO_D`, `AND.IMM_TO_D` |
| `REG3, SIZE2` / `EA6, REG3, SIZE2` | 0.667 | 34800 | `ABS.D`, `DEC.D`, `DJcc.D_TO_EA`, `MOVcc.D_TO_EA` |
| `REG3, SIZE2` / `REG3, REG3#2, SIZE2` | 0.667 | 34800 | `ABS.D`, `DEC.D`, `EXTSQ.D_TO_D`, `EXTZQ.D_TO_D` |
| `EA6, REG3, SIZE1` / `EA6, REG3` | 0.667 | 33666 | `MOV.D_TO_EA`, `MOV.EA_TO_D`, `LCALL.D_TO_EA`, `LJMP.D_TO_EA` |
| `EA6, REG3, SIZE2` / `EA6, REG3` | 0.667 | 33666 | `DJcc.D_TO_EA`, `MOVcc.D_TO_EA`, `LCALL.D_TO_EA`, `LJMP.D_TO_EA` |
| `EA6, REG3, SIZE2` / `EA6, SIZE2` | 0.667 | 14133 | `DJcc.D_TO_EA`, `MOVcc.D_TO_EA`, `SETcc.EA`, `ABS.EA` |
| `REG3, REG3#2, SIZE1` / `REG3, REG3#2` | 0.667 | 12240 | `ADD.D_TO_D`, `AND.D_TO_D`, `EXTSW.D_TO_D`, `RDSEG.S_TO_D` |
| `REG3, REG3#2, SIZE2` / `REG3, REG3#2` | 0.667 | 12240 | `EXTSQ.D_TO_D`, `EXTZQ.D_TO_D`, `EXTSW.D_TO_D`, `RDSEG.S_TO_D` |

## Primary Payload Allocations

| Payload Range | Slots | Candidate | Bits | Field Layout | Operands |
| --- | --- | --- | --- | --- | --- |
| `0x000` | 1 | `HALT` | 0 | none |  |
| `0x001` | 1 | `CALL.IMM32` | 0 | none | target:imm32 |
| `0x002` | 1 | `CALL.IMM64` | 0 | none | target:imm64 |
| `0x003` | 1 | `CALL.IMM16` | 0 | none | target:imm16 |
| `0x004` | 1 | `BKPT` | 0 | none |  |
| `0x005` | 1 | `AFENCE` | 0 | none |  |
| `0x006` | 1 | `WFENCE` | 0 | none |  |
| `0x007` | 1 | `RFENCE` | 0 | none |  |
| `0x008`..`0x00f` | 8 | `PUSH.D` | 3 | d[2:0] | reg:DREG |
| `0x010`..`0x01f` | 16 | `AND.IMM_TO_D` | 4 | d[2:0] z[3] | imm, dst:DREG |
| `0x020`..`0x03f` | 32 | `DEC.D` | 5 | d[2:0] s[4:3] | dst:DREG |
| `0x040`..`0x07f` | 64 | `EXTSW.D_TO_D` | 6 | d[2:0] D[5:3] | src:DREG, dst:DREG |
| `0x080`..`0x0ff` | 128 | `ADD.D_TO_D` | 7 | d[2:0] D[5:3] z[6] | src:DREG, dst:DREG |
| `0x100`..`0x1bf` | 192 | `EXTSQ.D_TO_D` | 8 | d[2:0] D[5:3] s[7:6] | src:DREG, dst:DREG |
| `0x1c0`..`0x1df` | 32 | `INC.D` | 5 | d[2:0] s[4:3] | dst:DREG |
| `0x1e0`..`0x1ff` | 32 | `ABS.D` | 5 | d[2:0] s[4:3] | dst:DREG |
| `0x200`..`0x2bf` | 192 | `EXTZQ.D_TO_D` | 8 | d[2:0] D[5:3] s[7:6] | src:DREG, dst:DREG |
| `0x2c0`..`0x2df` | 32 | `DECN.D` | 5 | d[2:0] s[4:3] | dst:DREG |
| `0x2e0`..`0x2ff` | 32 | `INCN.D` | 5 | d[2:0] s[4:3] | dst:DREG |
| `0x300`..`0x37f` | 128 | `AND.D_TO_D` | 7 | d[2:0] D[5:3] z[6] | src:DREG, dst:DREG |
| `0x380`..`0x3ff` | 128 | `CMP.D_TO_D` | 7 | d[2:0] D[5:3] z[6] | src:DREG, dst:DREG |
| `0x400`, `0x440`, `0x480`, `0x4c0`, `0x500`, `0x540`, `0x580`, `0x5c0`, `0x600`, `0x640`, `0x680`, `0x6c0`, `0x700`, `0x740`, `0x780`, `0x7c0` | 16 | `ADD.IMM_TO_D` | 10 | d[8:6] z[9] | imm, dst:DREG |
| `0x408`..`0x43f`, `0x448`..`0x47f`, `0x488`..`0x4bf`, `0x4c8`..`0x4ff`, `0x508`..`0x53f`, `0x548`..`0x57f`, `0x588`..`0x5bf`, `0x5c8`..`0x5ff`, `0x608`..`0x63f`, `0x648`..`0x67f`, `0x688`..`0x6bf`, `0x6c8`..`0x6ff`, `0x708`..`0x73f`, `0x748`..`0x77f`, `0x788`..`0x7bf`, `0x7c8`..`0x7ff` | 896 | `MOV.D_TO_EA` | 10 | e[5:0] d[8:6] z[9] | src:DREG, dst:EA |
| `0x401`, `0x441`, `0x481`, `0x4c1`, `0x501`, `0x541`, `0x581`, `0x5c1`, `0x601`, `0x641`, `0x681`, `0x6c1`, `0x701`, `0x741`, `0x781`, `0x7c1` | 16 | `CMP.IMM_TO_D` | 10 | d[8:6] z[9] | imm, rhs:DREG |
| `0x402`, `0x442`, `0x482`, `0x4c2`, `0x502`, `0x542`, `0x582`, `0x5c2`, `0x602`, `0x642`, `0x682`, `0x6c2`, `0x702`, `0x742`, `0x782`, `0x7c2` | 16 | `SUB.IMM_TO_D` | 10 | d[8:6] z[9] | imm, dst:DREG |
| `0x403`, `0x443`, `0x483`, `0x4c3`, `0x503`, `0x543`, `0x583`, `0x5c3`, `0x603`, `0x643`, `0x683`, `0x6c3`, `0x703`, `0x743`, `0x783`, `0x7c3` | 16 | `TEST.IMM_TO_D` | 10 | d[8:6] z[9] | imm, rhs:DREG |
| `0x800`..`0xbff` | 1024 | `MOV.EA_TO_D` | 10 | e[5:0] d[8:6] z[9] | src:EA, dst:DREG |
| `0xc00`..`0xc7f` | 128 | `OR.D_TO_D` | 7 | d[2:0] D[5:3] z[6] | src:DREG, dst:DREG |
| `0xc80`..`0xcff` | 128 | `SUB.D_TO_D` | 7 | d[2:0] D[5:3] z[6] | src:DREG, dst:DREG |
| `0xd00`..`0xd7f` | 128 | `TEST.D_TO_D` | 7 | d[2:0] D[5:3] z[6] | src:DREG, dst:DREG |
| `0xd80`..`0xdff` | 128 | `XOR.D_TO_D` | 7 | d[2:0] D[5:3] z[6] | src:DREG, dst:DREG |
| `0xe00`..`0xe7f` | 128 | `EXTZL.D_TO_D` | 7 | d[2:0] D[5:3] s[6] | src:DREG, dst:DREG |
| `0xe80`..`0xe9f` | 32 | `NEG.D` | 5 | d[2:0] s[4:3] | dst:DREG |
| `0xea0`..`0xebf` | 32 | `NOT.D` | 5 | d[2:0] s[4:3] | dst:DREG |
| `0xec0`, `0xec2`..`0xed0`, `0xed2`..`0xedf` | 30 | `Jcc.IMM` | 5 | c[3:0] z[4] | cc:condition, target:relative_imm |
| `0xec1` | 1 | `SYSCALL` | 0 | none |  |
| `0xed1` | 1 | `WAIT` | 0 | none |  |
| `0xee0`..`0xeef` | 16 | `OR.IMM_TO_D` | 4 | d[2:0] z[3] | imm, dst:DREG |
| `0xef0`..`0xeff` | 16 | `XOR.IMM_TO_D` | 4 | d[2:0] z[3] | imm, dst:DREG |
| `0xf00`..`0xf07` | 8 | `PUSH.A` | 3 | a[2:0] | reg:AREG |
| `0xf08`..`0xf0f` | 8 | `POP.D` | 3 | d[2:0] | reg:DREG |
| `0xf10`..`0xf17` | 8 | `POP.A` | 3 | a[2:0] | reg:AREG |
| `0xf18`..`0xf1f` | 8 | `CLR.A` | 3 | a[2:0] | dst:AREG |
| `0xf20`..`0xf27` | 8 | `CLR.D` | 3 | d[2:0] | dst:DREG |
| `0xf28`..`0xf2f` | 8 | `MOV.IMM_TO_A` | 3 | a[2:0] | src:imm64, dst:AREG |
| `0xf30` | 1 | `RET` | 0 | none |  |
| `0xf31` | 1 | `YIELD` | 0 | none |  |
| `0xf32` | 1 | `PUSHM.BITMAP` | 0 | none | regs:bitmap16 |
| `0xf33` | 1 | `POPM.BITMAP` | 0 | none | regs:bitmap16 |
| `0xf34` | 1 | `MOVSETAD.BITMAP` | 0 | none | regs:bitmap16 |
| `0xf35` | 1 | `MOVSETDA.BITMAP` | 0 | none | regs:bitmap16 |
| `0xf36` | 1 | `XCHGSETAD.BITMAP` | 0 | none | regs:bitmap16 |
| `0xf37` | 1 | `XCHGSETDA.BITMAP` | 0 | none | regs:bitmap16 |
| `0xf38` | 1 | `RESET` | 0 | none |  |
| `0xf39` | 1 | `SYSRET` | 0 | none |  |
| `0xf3a` | 1 | `IRET` | 0 | none |  |
| `0xf3b` | 1 | `TRACE.IMM` | 0 | none | marker:imm16 |
| `0xf3c` | 1 | `EXT.integer_alu` | 0 | subop/operands in following word |  |
| `0xf3d` | 1 | `EXT.integer_alu_reg_ea_wide` | 0 | subop/operands in following word |  |
| `0xf3e` | 1 | `EXT.integer_alu_imm_ea_arith_wide` | 0 | subop/operands in following word |  |
| `0xf3f` | 1 | `EXT.integer_alu_imm_ea_logic_wide` | 0 | subop/operands in following word |  |
| `0xf40` | 1 | `EXT.integer_alu_cmp_ea_wide` | 0 | subop/operands in following word |  |
| `0xf41` | 1 | `EXT.integer_extend_ea_wide` | 0 | subop/operands in following word |  |
| `0xf42` | 1 | `EXT.integer_bounds_signed` | 0 | subop/operands in following word |  |
| `0xf43` | 1 | `EXT.integer_bounds_unsigned` | 0 | subop/operands in following word |  |
| `0xf44` | 1 | `EXT.integer_mul_div` | 0 | subop/operands in following word |  |
| `0xf45` | 1 | `EXT.integer_mac` | 0 | subop/operands in following word |  |
| `0xf46` | 1 | `EXT.integer_bitfield` | 0 | subop/operands in following word |  |
| `0xf47` | 1 | `EXT.integer_bitfield_bit_imm` | 0 | subop/operands in following word |  |
| `0xf48` | 1 | `EXT.integer_bitfield_rotate_imm` | 0 | subop/operands in following word |  |
| `0xf49` | 1 | `EXT.integer_bitfield_shift_imm` | 0 | subop/operands in following word |  |
| `0xf4a` | 1 | `EXT.data_movement` | 0 | subop/operands in following word |  |
| `0xf4b` | 1 | `EXT.data_register_banking` | 0 | subop/operands in following word |  |
| `0xf4c` | 1 | `EXT.ea_utility` | 0 | subop/operands in following word |  |
| `0xf4d` | 1 | `EXT.control_flow` | 0 | subop/operands in following word |  |
| `0xf4f` | 1 | `NOP` | 0 | none |  |
| `0xf50`..`0xf5f` | 16 | `EXT.conditional_control.cc` | 4 | c[3:0] subop/operands in following word |  |
| `0xf60` | 1 | `EXT.atomic_memory` | 0 | subop/operands in following word |  |
| `0xf61` | 1 | `EXT.cache_hint` | 0 | subop/operands in following word |  |
| `0xf62` | 1 | `EXT.tlb_cache` | 0 | subop/operands in following word |  |
| `0xf63` | 1 | `EXT.system_core` | 0 | subop/operands in following word |  |
| `0xf64` | 1 | `EXT.virtualization_acceleration` | 0 | subop/operands in following word |  |
| `0xf65` | 1 | `EXT.fpu_move_compare` | 0 | subop/operands in following word |  |
| `0xf66` | 1 | `EXT.fpu_arithmetic_ea_wide` | 0 | subop/operands in following word |  |
| `0xf67` | 1 | `EXT.fpu_arithmetic` | 0 | subop/operands in following word |  |
| `0xf68` | 1 | `EXT.fpu_transcendental` | 0 | subop/operands in following word |  |
| `0xf70`..`0xf77` | 8 | `REPG.D_TO_IMM` | 3 | d[2:0] | counter:DREG, body_bytes:imm16 |
| `0xfff` | 1 | `ILLEGAL` | 0 | none |  |

## Extension Roots

| Payload Range | Root | Family | Profile | Primary Slots | Forms | Ext Slots Used | Ext Slots Free |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `0xf3c` | `EXT.integer_alu` | integer_alu | D_TO_D | 1 | 48 | 64256 | 1280 |
| `0xf3d` | `EXT.integer_alu_reg_ea_wide` | integer_alu_reg_ea_wide | EA_TO_D | 1 | 5 | 10240 | 55296 |
| `0xf3e` | `EXT.integer_alu_imm_ea_arith_wide` | integer_alu_imm_ea_arith_wide | IMM_TO_EA | 1 | 4 | 65536 | 0 |
| `0xf3f` | `EXT.integer_alu_imm_ea_logic_wide` | integer_alu_imm_ea_logic_wide | IMM_TO_EA | 1 | 4 | 65536 | 0 |
| `0xf40` | `EXT.integer_alu_cmp_ea_wide` | integer_alu_cmp_ea_wide | IMM_TO_EA | 1 | 2 | 32768 | 32768 |
| `0xf41` | `EXT.integer_extend_ea_wide` | integer_extend_ea_wide | EA_TO_EA | 1 | 6 | 57344 | 8192 |
| `0xf42` | `EXT.integer_bounds_signed` | integer_bounds_signed | D_TO_EA_TO_D | 1 | 4 | 65536 | 0 |
| `0xf43` | `EXT.integer_bounds_unsigned` | integer_bounds_unsigned | D_TO_EA_TO_D | 1 | 4 | 65536 | 0 |
| `0xf44` | `EXT.integer_mul_div` | integer_mul_div | EA_TO_D | 1 | 24 | 61441 | 4095 |
| `0xf45` | `EXT.integer_mac` | integer_mac | EA_TO_D_TO_D | 1 | 2 | 32768 | 32768 |
| `0xf46` | `EXT.integer_bitfield` | integer_bitfield | D_TO_D | 1 | 31 | 40192 | 25344 |
| `0xf47` | `EXT.integer_bitfield_bit_imm` | integer_bitfield_bit_imm | I6_TO_EA | 1 | 4 | 65536 | 0 |
| `0xf48` | `EXT.integer_bitfield_rotate_imm` | integer_bitfield_rotate_imm | I6_TO_EA | 1 | 4 | 65536 | 0 |
| `0xf49` | `EXT.integer_bitfield_shift_imm` | integer_bitfield_shift_imm | I6_TO_EA | 1 | 3 | 49152 | 16384 |
| `0xf4a` | `EXT.data_movement` | data_movement | EA_TO_EA | 1 | 5 | 24576 | 40960 |
| `0xf4b` | `EXT.data_register_banking` | data_register_banking | DB_TO_BITMAP | 1 | 9 | 608 | 64928 |
| `0xf4c` | `EXT.ea_utility` | ea_utility | EA_TO_A | 1 | 3 | 1088 | 64448 |
| `0xf4d` | `EXT.control_flow` | control_flow | D_TO_EA | 1 | 4 | 1089 | 64447 |
| `0xf50..0xf5f` | `EXT.conditional_control.cc` | conditional_control | D_TO_EA | 16 | 12 | 23169 | 42367 |
| `0xf60` | `EXT.atomic_memory` | atomic_memory | D_TO_D_TO_EA | 1 | 6 | 9 | 65527 |
| `0xf61` | `EXT.cache_hint` | cache_hint | EA | 1 | 1 | 64 | 65472 |
| `0xf62` | `EXT.tlb_cache` | tlb_cache | D | 1 | 14 | 658 | 64878 |
| `0xf63` | `EXT.system_core` | system_core | D | 1 | 14 | 336 | 65200 |
| `0xf64` | `EXT.virtualization_acceleration` | virtualization_acceleration | EA | 1 | 1 | 64 | 65472 |
| `0xf65` | `EXT.fpu_move_compare` | fpu_move_compare | F_TO_D | 1 | 15 | 8624 | 56912 |
| `0xf66` | `EXT.fpu_arithmetic_ea_wide` | fpu_arithmetic_ea_wide | EA_TO_F | 1 | 3 | 6144 | 59392 |
| `0xf67` | `EXT.fpu_arithmetic` | fpu_arithmetic | F_TO_F | 1 | 72 | 63847 | 1689 |
| `0xf68` | `EXT.fpu_transcendental` | fpu_transcendental | F_TO_F | 1 | 19 | 9728 | 55808 |

## Symmetry Audit

| Check | Status | Severity | Detail |
| --- | --- | --- | --- |
| integer_minmax_all_or_none | `pass` | medium | no integer min/max D_TO_D forms selected compact |
| integer_mul_div_compact_recommended_none | `pass` | medium | no integer MUL/DIV/MOD D_TO_D forms selected compact |
| stack_push_pop_nearby | `fail` | medium | span=3856 slots=32 count=4 |
| direct_call_immediates_clustered | `pass` | low | span=2 slots=2 count=2 |
| bitmap_ops_clustered | `pass` | medium | span=6 slots=6 count=6 |
| cache_hint_family | `pass` | medium | PREFETCH root=EXT.cache_hint |
| ea_utility_family | `pass` | medium | compact=none roots=['EXT.ea_utility'] |
| integer_alu_root_locality | `pass` | medium | family_roots=['EXT.integer_alu'] profiles=[] payloads=[] span=0 slots=0 |
| fpu_compare_pair_EXT.fpu_move_compare | `pass` | low | FCMP.F_TO_F[F]=0x0000..0x01ff FTEST.F=0x0200..0x021f; FCMP.EA_TO_F[EA]=0x0800..0x0fff FTEST.EA=0x1000..0x107f |

## Conditional Alias Audit

| Check | Status | Detail |
| --- | --- | --- |
| JMP_aliases_Jcc_T | `pass` | aliases=['JMP.EA', 'JMP.IMM'] |
| TRAP_aliases_TRAPcc_T | `pass` | aliases=['TRAP'] |

## Canonical Alias Allocations

| Alias | Alias Of | Condition | Encoding | Notes |
| --- | --- | --- | --- | --- |
| `JMP.IMM` | `Jcc.IMM` | `T` | primary `0xec0`, `0xed0` | canonical disassembly `JMP` |
| `TRAP` | `TRAPcc` | `T` | EXT.conditional_control.cc @ `0xf50`; ext `0x0900` | canonical disassembly `TRAP` |
| `JMP.EA` | `Jcc.EA` | `T` | EXT.conditional_control.cc @ `0xf50`; ext `0x0980..0x09ff` | canonical disassembly `JMP` |

## Extended Opcode Allocations

| Root | Ext Opcode Range | Ext Slots | Candidate | Ext Field Bits | Payload Bits | Payload Words | Field Layout | Compact Cost If One-Word |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `EXT.integer_alu` | `0x0000..0x00ff` | 256 | `ABS.EA` | 8 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_alu` | `0x0100..0x013f` | 64 | `CLR.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.integer_alu` | `0x0140..0x015f` | 32 | `SUM.BITMAP_TO_A` | 5 | 16 | 1 | a:AREG[2:0], s:BWLQ[4:3], b:bitmap16/16@payload | policy-disabled |
| `EXT.integer_alu` | `0x0160..0x017f` | 32 | `SUM.BITMAP_TO_D` | 5 | 16 | 1 | d:DREG[2:0], s:BWLQ[4:3], b:bitmap16/16@payload | policy-disabled |
| `EXT.integer_alu` | `0x0180..0x01ff` | 128 | `EXTSL.D_TO_D` | 7 | 0 | 0 | d:DREG[2:0], D:DREG[5:3], s:BW[6] | 128 |
| `EXT.integer_alu` | `0x0200..0x03ff` | 512 | `ADD.EA_TO_A` | 9 | 0 | 0 | e:EA[5:0], a:AREG[8:6] | policy-disabled |
| `EXT.integer_alu` | `0x0400..0x05ff` | 512 | `CMP.EA_TO_A` | 9 | 0 | 0 | e:EA[5:0], a:AREG[8:6] | policy-disabled |
| `EXT.integer_alu` | `0x0600..0x06ff` | 256 | `DEC.EA` | 8 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_alu` | `0x0700..0x07ff` | 256 | `DECN.EA` | 8 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_alu` | `0x0800..0x0fff` | 2048 | `AND.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x1000..0x17ff` | 2048 | `CMP.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x1800..0x1fff` | 2048 | `CMP.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x2000..0x23ff` | 1024 | `EXTSL.D_TO_EA` | 10 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BW[9] | policy-disabled |
| `EXT.integer_alu` | `0x2400..0x27ff` | 1024 | `EXTSL.EA_TO_D` | 10 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BW[9] | policy-disabled |
| `EXT.integer_alu` | `0x2800..0x2fff` | 2048 | `EXTSQ.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWL[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x3000..0x37ff` | 2048 | `EXTSQ.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWL[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x3800..0x39ff` | 512 | `EXTSW.D_TO_EA` | 9 | 0 | 0 | e:EA[5:0], d:DREG[8:6] | policy-disabled |
| `EXT.integer_alu` | `0x3a00..0x3bff` | 512 | `EXTSW.EA_TO_D` | 9 | 0 | 0 | e:EA[5:0], d:DREG[8:6] | policy-disabled |
| `EXT.integer_alu` | `0x3c00..0x3fff` | 1024 | `EXTZL.D_TO_EA` | 10 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BW[9] | policy-disabled |
| `EXT.integer_alu` | `0x4000..0x43ff` | 1024 | `EXTZL.EA_TO_D` | 10 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BW[9] | policy-disabled |
| `EXT.integer_alu` | `0x4400..0x44ff` | 256 | `INC.EA` | 8 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_alu` | `0x4500..0x45ff` | 256 | `INCN.EA` | 8 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_alu` | `0x4600..0x46ff` | 256 | `NEG.EA` | 8 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_alu` | `0x4700..0x47ff` | 256 | `NOT.EA` | 8 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_alu` | `0x4800..0x4fff` | 2048 | `EXTZQ.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWL[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x5000..0x57ff` | 2048 | `EXTZQ.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWL[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x5800..0x5fff` | 2048 | `MAXS.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x6000..0x67ff` | 2048 | `MAXS.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x6800..0x6fff` | 2048 | `MAXU.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x7000..0x77ff` | 2048 | `MAXU.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x7800..0x7fff` | 2048 | `MINS.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x8000..0x87ff` | 2048 | `MINS.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x8800..0x8fff` | 2048 | `MINU.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x9000..0x97ff` | 2048 | `MINU.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0x9800..0x9fff` | 2048 | `OR.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0xa000..0xa7ff` | 2048 | `OR.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0xa800..0xa8ff` | 256 | `REVBYTE.D_TO_D` | 8 | 0 | 0 | d:DREG[2:0], D:DREG[5:3], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_alu` | `0xaa00..0xabff` | 512 | `SUB.EA_TO_A` | 9 | 0 | 0 | e:EA[5:0], a:AREG[8:6] | policy-disabled |
| `EXT.integer_alu` | `0xb000..0xb7ff` | 2048 | `REVBYTE.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0xb800..0xbfff` | 2048 | `REVBYTE.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0xc000..0xc7ff` | 2048 | `SBB.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0xc800..0xcfff` | 2048 | `SBB.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0xd000..0xd7ff` | 2048 | `SUB.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0xd800..0xdfff` | 2048 | `SUB.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0xe000..0xe7ff` | 2048 | `TEST.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0xe800..0xefff` | 2048 | `TEST.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0xf000..0xf7ff` | 2048 | `XOR.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu` | `0xf800..0xffff` | 2048 | `XOR.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu_reg_ea_wide` | `0x0000..0x07ff` | 2048 | `ADC.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu_reg_ea_wide` | `0x0800..0x0fff` | 2048 | `ADC.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu_reg_ea_wide` | `0x1000..0x17ff` | 2048 | `ADD.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu_reg_ea_wide` | `0x1800..0x1fff` | 2048 | `ADD.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu_reg_ea_wide` | `0x2000..0x27ff` | 2048 | `AND.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_alu_imm_ea_arith_wide` | `0x0000..0x3fff` | 16384 | `ADC.IMM_TO_EA` | 14 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | bits=14>12 |
| `EXT.integer_alu_imm_ea_arith_wide` | `0x4000..0x7fff` | 16384 | `ADD.IMM_TO_EA` | 14 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | bits=14>12 |
| `EXT.integer_alu_imm_ea_arith_wide` | `0x8000..0xbfff` | 16384 | `SBB.IMM_TO_EA` | 14 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | bits=14>12 |
| `EXT.integer_alu_imm_ea_arith_wide` | `0xc000..0xffff` | 16384 | `SUB.IMM_TO_EA` | 14 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | bits=14>12 |
| `EXT.integer_alu_imm_ea_logic_wide` | `0x0000..0x3fff` | 16384 | `AND.IMM_TO_EA` | 14 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | bits=14>12 |
| `EXT.integer_alu_imm_ea_logic_wide` | `0x4000..0x7fff` | 16384 | `OR.IMM_TO_EA` | 14 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | bits=14>12 |
| `EXT.integer_alu_imm_ea_logic_wide` | `0x8000..0xbfff` | 16384 | `TEST.IMM_TO_EA` | 14 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | bits=14>12 |
| `EXT.integer_alu_imm_ea_logic_wide` | `0xc000..0xffff` | 16384 | `XOR.IMM_TO_EA` | 14 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | bits=14>12 |
| `EXT.integer_alu_cmp_ea_wide` | `0x0000..0x3fff` | 16384 | `CMP.EA_TO_EA` | 14 | 0 | 0 | e:EA[5:0], E:EA[11:6], s:BWLQ[13:12] | bits=14>12 |
| `EXT.integer_alu_cmp_ea_wide` | `0x4000..0x7fff` | 16384 | `CMP.IMM_TO_EA` | 14 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | bits=14>12 |
| `EXT.integer_extend_ea_wide` | `0x0000..0x1fff` | 8192 | `EXTSL.EA_TO_EA` | 13 | 0 | 0 | e:EA[5:0], E:EA[11:6], s:BW[12] | bits=13>12 |
| `EXT.integer_extend_ea_wide` | `0x2000..0x2fff` | 4096 | `EXTSW.EA_TO_EA` | 12 | 0 | 0 | e:EA[5:0], E:EA[11:6] | policy-disabled |
| `EXT.integer_extend_ea_wide` | `0x3000..0x3fff` | 4096 | `EXTZW.EA_TO_EA` | 12 | 0 | 0 | e:EA[5:0], E:EA[11:6] | policy-disabled |
| `EXT.integer_extend_ea_wide` | `0x4000..0x7fff` | 16384 | `EXTSQ.EA_TO_EA` | 14 | 0 | 0 | e:EA[5:0], E:EA[11:6], s:BWL[13:12] | bits=14>12 |
| `EXT.integer_extend_ea_wide` | `0x8000..0x9fff` | 8192 | `EXTZL.EA_TO_EA` | 13 | 0 | 0 | e:EA[5:0], E:EA[11:6], s:BW[12] | bits=13>12 |
| `EXT.integer_extend_ea_wide` | `0xc000..0xffff` | 16384 | `EXTZQ.EA_TO_EA` | 14 | 0 | 0 | e:EA[5:0], E:EA[11:6], s:BWL[13:12] | bits=14>12 |
| `EXT.integer_bounds_signed` | `0x0000..0x3fff` | 16384 | `BNDSII.D_TO_EA_TO_D` | 14 | 0 | 0 | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | bits=14>12 |
| `EXT.integer_bounds_signed` | `0x4000..0x7fff` | 16384 | `BNDSIX.D_TO_EA_TO_D` | 14 | 0 | 0 | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | bits=14>12 |
| `EXT.integer_bounds_signed` | `0x8000..0xbfff` | 16384 | `BNDSXI.D_TO_EA_TO_D` | 14 | 0 | 0 | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | bits=14>12 |
| `EXT.integer_bounds_signed` | `0xc000..0xffff` | 16384 | `BNDSXX.D_TO_EA_TO_D` | 14 | 0 | 0 | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | bits=14>12 |
| `EXT.integer_bounds_unsigned` | `0x0000..0x3fff` | 16384 | `BNDUII.D_TO_EA_TO_D` | 14 | 0 | 0 | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | bits=14>12 |
| `EXT.integer_bounds_unsigned` | `0x4000..0x7fff` | 16384 | `BNDUIX.D_TO_EA_TO_D` | 14 | 0 | 0 | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | bits=14>12 |
| `EXT.integer_bounds_unsigned` | `0x8000..0xbfff` | 16384 | `BNDUXI.D_TO_EA_TO_D` | 14 | 0 | 0 | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | bits=14>12 |
| `EXT.integer_bounds_unsigned` | `0xc000..0xffff` | 16384 | `BNDUXX.D_TO_EA_TO_D` | 14 | 0 | 0 | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | bits=14>12 |
| `EXT.integer_mul_div` | `0x0000..0x07ff` | 2048 | `CLMUL.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0x0800..0x0fff` | 2048 | `CLMUL.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0x1000..0x17ff` | 2048 | `CLMULH.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0x1800..0x1fff` | 2048 | `CLMULH.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0x2000` | 1 | `DIVMODS.EA_TO_D_TO_D` | 0 | 14+spill | 1 | e:EA/6@payload, d:DREG/3@payload, D:DREG/3@payload, s:BWLQ/2@payload | bits=14>12 |
| `EXT.integer_mul_div` | `0x2800..0x2fff` | 2048 | `DIVS.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0x3000..0x37ff` | 2048 | `DIVS.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0x3800..0x3fff` | 2048 | `DIVU.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0x4000..0x7fff` | 16384 | `DIVMODU.EA_TO_D_TO_D` | 14 | 0 | 0 | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | bits=14>12 |
| `EXT.integer_mul_div` | `0x8000..0x87ff` | 2048 | `DIVU.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0x8800..0x8fff` | 2048 | `MODS.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0x9000..0x97ff` | 2048 | `MODS.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0x9800..0x9fff` | 2048 | `MODU.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0xa000..0xa7ff` | 2048 | `MODU.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0xa800..0xafff` | 2048 | `MULHS.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0xb000..0xb7ff` | 2048 | `MULHS.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0xb800..0xbfff` | 2048 | `MULHSU.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0xc000..0xc7ff` | 2048 | `MULHSU.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0xc800..0xcfff` | 2048 | `MULHU.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0xd000..0xd7ff` | 2048 | `MULHU.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0xd800..0xdfff` | 2048 | `MULS.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0xe000..0xe7ff` | 2048 | `MULS.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0xe800..0xefff` | 2048 | `MULU.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mul_div` | `0xf000..0xf7ff` | 2048 | `MULU.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_mac` | `0x0000..0x3fff` | 16384 | `MADD.EA_TO_D_TO_D` | 14 | 0 | 0 | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | bits=14>12 |
| `EXT.integer_mac` | `0x4000..0x7fff` | 16384 | `MSUB.EA_TO_D_TO_D` | 14 | 0 | 0 | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | bits=14>12 |
| `EXT.integer_bitfield` | `0x0000..0x00ff` | 256 | `BCHG.D_TO_D` | 8 | 0 | 0 | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_bitfield` | `0x0100..0x01ff` | 256 | `BCLR.D_TO_D` | 8 | 0 | 0 | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_bitfield` | `0x0200..0x02ff` | 256 | `BSET.D_TO_D` | 8 | 0 | 0 | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_bitfield` | `0x0300..0x03ff` | 256 | `BTEST.D_TO_D` | 8 | 0 | 0 | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_bitfield` | `0x0400..0x04ff` | 256 | `PARITY.EA` | 8 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_bitfield` | `0x0500..0x05ff` | 256 | `RCL.D_TO_D` | 8 | 0 | 0 | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_bitfield` | `0x0600..0x06ff` | 256 | `RCR.D_TO_D` | 8 | 0 | 0 | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_bitfield` | `0x0700..0x07ff` | 256 | `REVBIT.D_TO_D` | 8 | 0 | 0 | d:DREG[2:0], D:DREG[5:3], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_bitfield` | `0x0800..0x0fff` | 2048 | `BCHG.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_bitfield` | `0x1000..0x17ff` | 2048 | `BCLR.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_bitfield` | `0x1800..0x1fff` | 2048 | `BSET.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_bitfield` | `0x2000..0x27ff` | 2048 | `BTEST.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_bitfield` | `0x2800..0x2fff` | 2048 | `CLS.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_bitfield` | `0x3000..0x37ff` | 2048 | `CLZ.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_bitfield` | `0x3800..0x3fff` | 2048 | `CTS.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_bitfield` | `0x4000..0x47ff` | 2048 | `CTZ.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_bitfield` | `0x4800..0x4fff` | 2048 | `POPCNT.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.integer_bitfield` | `0x5000..0x57ff` | 2048 | `RCL.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_bitfield` | `0x5800..0x5fff` | 2048 | `RCR.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_bitfield` | `0x6000..0x67ff` | 2048 | `REVBIT.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_bitfield` | `0x6800..0x6fff` | 2048 | `REVBIT.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_bitfield` | `0x7000..0x70ff` | 256 | `ROL.D_TO_D` | 8 | 0 | 0 | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_bitfield` | `0x7100..0x71ff` | 256 | `ROR.D_TO_D` | 8 | 0 | 0 | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_bitfield` | `0x7200..0x72ff` | 256 | `SAR.D_TO_D` | 8 | 0 | 0 | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_bitfield` | `0x7300..0x73ff` | 256 | `SHL.D_TO_D` | 8 | 0 | 0 | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_bitfield` | `0x7400..0x74ff` | 256 | `SHR.D_TO_D` | 8 | 0 | 0 | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | policy-disabled |
| `EXT.integer_bitfield` | `0x7800..0x7fff` | 2048 | `ROL.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_bitfield` | `0x8000..0x87ff` | 2048 | `ROR.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_bitfield` | `0x8800..0x8fff` | 2048 | `SAR.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_bitfield` | `0x9000..0x97ff` | 2048 | `SHL.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_bitfield` | `0x9800..0x9fff` | 2048 | `SHR.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.integer_bitfield_bit_imm` | `0x0000..0x3fff` | 16384 | `BCHG.I6_TO_EA` | 14 | 0 | 0 | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:bit_group=BCHG[15:14] | bits=14>12 |
| `EXT.integer_bitfield_bit_imm` | `0x4000..0x7fff` | 16384 | `BCLR.I6_TO_EA` | 14 | 0 | 0 | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:bit_group=BCLR[15:14] | bits=14>12 |
| `EXT.integer_bitfield_bit_imm` | `0x8000..0xbfff` | 16384 | `BSET.I6_TO_EA` | 14 | 0 | 0 | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:bit_group=BSET[15:14] | bits=14>12 |
| `EXT.integer_bitfield_bit_imm` | `0xc000..0xffff` | 16384 | `BTEST.I6_TO_EA` | 14 | 0 | 0 | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:bit_group=BTEST[15:14] | bits=14>12 |
| `EXT.integer_bitfield_rotate_imm` | `0x0000..0x3fff` | 16384 | `RCL.I6_TO_EA` | 14 | 0 | 0 | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:rotate_group=RCL[15:14] | bits=14>12 |
| `EXT.integer_bitfield_rotate_imm` | `0x4000..0x7fff` | 16384 | `RCR.I6_TO_EA` | 14 | 0 | 0 | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:rotate_group=RCR[15:14] | bits=14>12 |
| `EXT.integer_bitfield_rotate_imm` | `0x8000..0xbfff` | 16384 | `ROL.I6_TO_EA` | 14 | 0 | 0 | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:rotate_group=ROL[15:14] | bits=14>12 |
| `EXT.integer_bitfield_rotate_imm` | `0xc000..0xffff` | 16384 | `ROR.I6_TO_EA` | 14 | 0 | 0 | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:rotate_group=ROR[15:14] | bits=14>12 |
| `EXT.integer_bitfield_shift_imm` | `0x0000..0x3fff` | 16384 | `SHL.I6_TO_EA` | 14 | 0 | 0 | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:shift_group=SHL[15:14] | bits=14>12 |
| `EXT.integer_bitfield_shift_imm` | `0x4000..0x7fff` | 16384 | `SHR.I6_TO_EA` | 14 | 0 | 0 | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:shift_group=SHR[15:14] | bits=14>12 |
| `EXT.integer_bitfield_shift_imm` | `0x8000..0xbfff` | 16384 | `SAR.I6_TO_EA` | 14 | 0 | 0 | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:shift_group=SAR[15:14] | bits=14>12 |
| `EXT.data_movement` | `0x0000..0x07ff` | 2048 | `MOV.D_TO_EA_WIDE` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.data_movement` | `0x0800..0x0fff` | 2048 | `MOV.EA_TO_D_WIDE` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | policy-disabled |
| `EXT.data_movement` | `0x1000..0x17ff` | 2048 | `XCHG.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.data_movement` | `0x1800..0x1fff` | 2048 | `XCHG.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | 2048 |
| `EXT.data_movement` | `0x4000..0x7fff` | 16384 | `MOV.EA_TO_EA` | 14 | 0 | 0 | e:EA[5:0], E:EA[11:6], s:BWLQ[13:12] | bits=14>12 |
| `EXT.data_register_banking` | `0x0000..0x0007` | 8 | `GETDB.D` | 3 | 0 | 0 | d:DREG[2:0] | policy-disabled |
| `EXT.data_register_banking` | `0x0008..0x000f` | 8 | `SELDB.D` | 3 | 0 | 0 | d:DREG[2:0] | policy-disabled |
| `EXT.data_register_banking` | `0x0010..0x001f` | 16 | `MOVSETAD.DB_TO_BITMAP` | 4 | 16 | 1 | k:DBANK[3:0], b:bitmap16/16@payload | policy-disabled |
| `EXT.data_register_banking` | `0x0020..0x002f` | 16 | `MOVSETDA.DB_TO_BITMAP` | 4 | 16 | 1 | k:DBANK[3:0], b:bitmap16/16@payload | policy-disabled |
| `EXT.data_register_banking` | `0x0030..0x003f` | 16 | `SELDB.DB` | 4 | 0 | 0 | k:DBANK[3:0] | policy-disabled |
| `EXT.data_register_banking` | `0x0040..0x004f` | 16 | `XCHGSETAD.DB_TO_BITMAP` | 4 | 16 | 1 | k:DBANK[3:0], b:bitmap16/16@payload | policy-disabled |
| `EXT.data_register_banking` | `0x0050..0x005f` | 16 | `XCHGSETDA.DB_TO_BITMAP` | 4 | 16 | 1 | k:DBANK[3:0], b:bitmap16/16@payload | policy-disabled |
| `EXT.data_register_banking` | `0x0100..0x01ff` | 256 | `MOVSETDD.DB_TO_DB_TO_BITMAP` | 8 | 16 | 1 | k:DBANK[3:0], K:DBANK[7:4], b:bitmap16/16@payload | policy-disabled |
| `EXT.data_register_banking` | `0x0200..0x02ff` | 256 | `XCHGSETDD.DB_TO_DB_TO_BITMAP` | 8 | 16 | 1 | k:DBANK[3:0], K:DBANK[7:4], b:bitmap16/16@payload | policy-disabled |
| `EXT.ea_utility` | `0x0000..0x01ff` | 512 | `LEA.EA_TO_A` | 9 | 0 | 0 | e:EA[5:0], a:AREG[8:6] | 512 |
| `EXT.ea_utility` | `0x0200..0x03ff` | 512 | `SEGLEA.EA_TO_A` | 9 | 0 | 0 | e:EA[5:0], a:AREG[8:6] | 512 |
| `EXT.ea_utility` | `0x0400..0x043f` | 64 | `TESTCANON.EA` | 6 | 0 | 0 | e:EA[5:0] | 64 |
| `EXT.control_flow` | `0x0000..0x003f` | 64 | `CALL.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.control_flow` | `0x0040` | 1 | `LRET` | 0 | 0 | 0 | none | policy-disabled |
| `EXT.control_flow` | `0x0200..0x03ff` | 512 | `LCALL.D_TO_EA` | 9 | 0 | 0 | e:EA[5:0], d:DREG[8:6] | policy-disabled |
| `EXT.control_flow` | `0x0400..0x05ff` | 512 | `LJMP.D_TO_EA` | 9 | 0 | 0 | e:EA[5:0], d:DREG[8:6] | policy-disabled |
| `EXT.conditional_control.cc` | `0x0000..0x07ff` | 2048 | `DJcc.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9], c:condition/4@root | bits=15>12 |
| `EXT.conditional_control.cc` | `0x0800..0x08ff` | 256 | `FMOVcc.F_TO_F` | 8 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], c:condition/4@root | policy-disabled |
| `EXT.conditional_control.cc` | `0x0900` | 1 | `TRAPcc` | 0 | 0 | 0 | c:condition/4@root | 16 |
| `EXT.conditional_control.cc` | `0x0980..0x09ff` | 128 | `Jcc.EA` | 7 | 0 | 0 | e:EA[5:0], z:WL[6], c:condition/4@root | policy-disabled |
| `EXT.conditional_control.cc` | `0x0a00..0x0aff` | 256 | `SETcc.EA` | 8 | 0 | 0 | e:EA[5:0], s:BWLQ[7:6], c:condition/4@root | 4096 |
| `EXT.conditional_control.cc` | `0x1000..0x17ff` | 2048 | `MOVcc.A_TO_EA` | 11 | 0 | 0 | e:EA[5:0], a:AREG[8:6], s:BWLQ[10:9], c:condition/4@root | bits=15>12 |
| `EXT.conditional_control.cc` | `0x1800..0x1fff` | 2048 | `MOVcc.D_TO_EA` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9], c:condition/4@root | bits=15>12 |
| `EXT.conditional_control.cc` | `0x2000..0x3fff` | 8192 | `IJcc.D_TO_D_TO_EA` | 13 | 0 | 0 | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], z:LQ[12], c:condition/4@root | bits=17>12 |
| `EXT.conditional_control.cc` | `0x4000..0x47ff` | 2048 | `MOVcc.EA_TO_A` | 11 | 0 | 0 | e:EA[5:0], a:AREG[8:6], s:BWLQ[10:9], c:condition/4@root | bits=15>12 |
| `EXT.conditional_control.cc` | `0x4800..0x4fff` | 2048 | `MOVcc.EA_TO_D` | 11 | 0 | 0 | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9], c:condition/4@root | bits=15>12 |
| `EXT.conditional_control.cc` | `0x5000..0x57ff` | 2048 | `FMOVcc.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10], c:condition/4@root | bits=15>12 |
| `EXT.conditional_control.cc` | `0x5800..0x5fff` | 2048 | `FMOVcc.F_TO_EA` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10], c:condition/4@root | bits=15>12 |
| `EXT.atomic_memory` | `0x0000..0x0003` | 4 | `CMPXCHG.D_TO_D_TO_EA` | 2 | 15+spill | 1 | s:BWLQ[1:0], o:memory_order/3@payload, e:EA/6@payload, d:DREG/3@payload, D:DREG/3@payload | bits=14>12 |
| `EXT.atomic_memory` | `0x0004` | 1 | `FETCHADD.D_TO_EA` | 0 | 14+spill | 1 | o:memory_order/3@payload, e:EA/6@payload, d:DREG/3@payload, s:BWLQ/2@payload | policy-disabled |
| `EXT.atomic_memory` | `0x0005` | 1 | `FETCHAND.D_TO_EA` | 0 | 14+spill | 1 | o:memory_order/3@payload, e:EA/6@payload, d:DREG/3@payload, s:BWLQ/2@payload | policy-disabled |
| `EXT.atomic_memory` | `0x0006` | 1 | `FETCHOR.D_TO_EA` | 0 | 14+spill | 1 | o:memory_order/3@payload, e:EA/6@payload, d:DREG/3@payload, s:BWLQ/2@payload | policy-disabled |
| `EXT.atomic_memory` | `0x0007` | 1 | `FETCHSUB.D_TO_EA` | 0 | 14+spill | 1 | o:memory_order/3@payload, e:EA/6@payload, d:DREG/3@payload, s:BWLQ/2@payload | policy-disabled |
| `EXT.atomic_memory` | `0x0008` | 1 | `FETCHXOR.D_TO_EA` | 0 | 14+spill | 1 | o:memory_order/3@payload, e:EA/6@payload, d:DREG/3@payload, s:BWLQ/2@payload | policy-disabled |
| `EXT.cache_hint` | `0x0000..0x003f` | 64 | `PREFETCH.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.tlb_cache` | `0x0000` | 1 | `INVTLB` | 0 | 0 | 0 | none | policy-disabled |
| `EXT.tlb_cache` | `0x0001` | 1 | `INVASID.IMM` | 0 | 16 | 1 | i:IMM16/16@payload | policy-disabled |
| `EXT.tlb_cache` | `0x0008..0x000f` | 8 | `SWPT.D` | 3 | 0 | 0 | d:DREG[2:0] | policy-disabled |
| `EXT.tlb_cache` | `0x0010..0x0017` | 8 | `RDPTC.D` | 3 | 0 | 0 | d:DREG[2:0] | policy-disabled |
| `EXT.tlb_cache` | `0x0040..0x007f` | 64 | `INVPAGE.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.tlb_cache` | `0x0080..0x00bf` | 64 | `SWPTA.D_TO_D` | 6 | 0 | 0 | d:DREG[2:0], D:DREG[5:3] | policy-disabled |
| `EXT.tlb_cache` | `0x00c0..0x00ff` | 64 | `INVDCACHE.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.tlb_cache` | `0x0100..0x013f` | 64 | `WRBKDCACHE.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.tlb_cache` | `0x0140..0x017f` | 64 | `FLSHDCACHE.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.tlb_cache` | `0x0180..0x01bf` | 64 | `INVICACHE.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.tlb_cache` | `0x01c0..0x01ff` | 64 | `SYNCCACHE.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.tlb_cache` | `0x0200..0x023f` | 64 | `PTATTR.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.tlb_cache` | `0x0240..0x027f` | 64 | `PTQUERY.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.tlb_cache` | `0x0280..0x02bf` | 64 | `VTOP.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.system_core` | `0x0000..0x0007` | 8 | `RDCR.D` | 3 | 16 | 1 | d:DREG[2:0], i:CR/16@payload | policy-disabled |
| `EXT.system_core` | `0x0008..0x000f` | 8 | `WRCR.D` | 3 | 16 | 1 | d:DREG[2:0], i:CR/16@payload | policy-disabled |
| `EXT.system_core` | `0x0010..0x0017` | 8 | `RDFLAGS.D` | 3 | 0 | 0 | d:DREG[2:0] | policy-disabled |
| `EXT.system_core` | `0x0018..0x001f` | 8 | `WRFLAGS.D` | 3 | 0 | 0 | d:DREG[2:0] | policy-disabled |
| `EXT.system_core` | `0x0020..0x0027` | 8 | `RDSTATUS.D` | 3 | 0 | 0 | d:DREG[2:0] | policy-disabled |
| `EXT.system_core` | `0x0028..0x002f` | 8 | `WRSTATUS.D` | 3 | 0 | 0 | d:DREG[2:0] | policy-disabled |
| `EXT.system_core` | `0x0030..0x0037` | 8 | `CPUID.D` | 3 | 0 | 0 | d:DREG[2:0] | policy-disabled |
| `EXT.system_core` | `0x0038..0x003f` | 8 | `RDFSTATUS.D` | 3 | 0 | 0 | d:DREG[2:0] | policy-disabled |
| `EXT.system_core` | `0x0040..0x007f` | 64 | `RDSEG.S_TO_D` | 6 | 0 | 0 | g:SREG[2:0], d:DREG[5:3] | policy-disabled |
| `EXT.system_core` | `0x0080..0x00bf` | 64 | `WRSEG.D_TO_S` | 6 | 0 | 0 | d:DREG[2:0], g:SREG[5:3] | policy-disabled |
| `EXT.system_core` | `0x00c0..0x00ff` | 64 | `SAVE.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.system_core` | `0x0100..0x013f` | 64 | `RESTORE.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.system_core` | `0x0140..0x0147` | 8 | `RDPMC.IMM_TO_D` | 3 | 16 | 1 | d:DREG[2:0], i:IMM16/16@payload | policy-disabled |
| `EXT.system_core` | `0x0148..0x014f` | 8 | `WRFSTATUS.D` | 3 | 0 | 0 | d:DREG[2:0] | policy-disabled |
| `EXT.virtualization_acceleration` | `0x0000..0x003f` | 64 | `ENCINST.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.fpu_move_compare` | `0x0000..0x01ff` | 512 | `FCMP.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_move_compare` | `0x0200..0x021f` | 32 | `FTEST.F` | 5 | 0 | 0 | f:FREG[3:0], z:S_D[4] | policy-disabled |
| `EXT.fpu_move_compare` | `0x0220..0x022f` | 16 | `FMOVCR.IMM_TO_F` | 4 | 16 | 1 | f:FREG[3:0], i:IMM16/16@payload | policy-disabled |
| `EXT.fpu_move_compare` | `0x0280..0x02ff` | 128 | `FCVT.D_TO_F` | 7 | 0 | 0 | d:DREG[2:0], f:FREG[6:3] | policy-disabled |
| `EXT.fpu_move_compare` | `0x0300..0x03ff` | 256 | `FCLASS.F_TO_D` | 8 | 0 | 0 | d:DREG[2:0], f:FREG[6:3], z:S_D[7] | policy-disabled |
| `EXT.fpu_move_compare` | `0x0400..0x05ff` | 512 | `FMOV.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_move_compare` | `0x0600..0x067f` | 128 | `FCVT.F_TO_D` | 7 | 0 | 0 | d:DREG[2:0], f:FREG[6:3] | policy-disabled |
| `EXT.fpu_move_compare` | `0x0680..0x06ff` | 128 | `FCVTU.D_TO_F` | 7 | 0 | 0 | d:DREG[2:0], f:FREG[6:3] | policy-disabled |
| `EXT.fpu_move_compare` | `0x0700..0x07ff` | 256 | `FCVT.F_TO_F` | 8 | 0 | 0 | f:FREG[3:0], F:FREG[7:4] | policy-disabled |
| `EXT.fpu_move_compare` | `0x0800..0x0fff` | 2048 | `FCMP.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_move_compare` | `0x1000..0x107f` | 128 | `FTEST.EA` | 7 | 0 | 0 | e:EA[5:0], z:S_D[6] | policy-disabled |
| `EXT.fpu_move_compare` | `0x1080..0x10ff` | 128 | `FCVTU.F_TO_D` | 7 | 0 | 0 | d:DREG[2:0], f:FREG[6:3] | policy-disabled |
| `EXT.fpu_move_compare` | `0x1100..0x11ff` | 256 | `FCVTU.F_TO_F` | 8 | 0 | 0 | f:FREG[3:0], F:FREG[7:4] | policy-disabled |
| `EXT.fpu_move_compare` | `0x1800..0x1fff` | 2048 | `FMOV.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_move_compare` | `0x2000..0x27ff` | 2048 | `FMOV.F_TO_EA` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic_ea_wide` | `0x0000..0x07ff` | 2048 | `FABS.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic_ea_wide` | `0x0800..0x0fff` | 2048 | `FABS.F_TO_EA` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic_ea_wide` | `0x1000..0x17ff` | 2048 | `FADD.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x0000..0x01ff` | 512 | `FABS.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x0200..0x03ff` | 512 | `FADD.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x0400` | 1 | `FBNDII.F_TO_EA_TO_F` | 0 | 15+spill | 1 | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | bits=15>12 |
| `EXT.fpu_arithmetic` | `0x0401` | 1 | `FBNDII.F_TO_F_TO_F` | 0 | 13+spill | 1 | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | bits=13>12 |
| `EXT.fpu_arithmetic` | `0x0402` | 1 | `FBNDIX.F_TO_EA_TO_F` | 0 | 15+spill | 1 | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | bits=15>12 |
| `EXT.fpu_arithmetic` | `0x0403` | 1 | `FBNDIX.F_TO_F_TO_F` | 0 | 13+spill | 1 | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | bits=13>12 |
| `EXT.fpu_arithmetic` | `0x0404` | 1 | `FBNDXI.F_TO_EA_TO_F` | 0 | 15+spill | 1 | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | bits=15>12 |
| `EXT.fpu_arithmetic` | `0x0405` | 1 | `FBNDXI.F_TO_F_TO_F` | 0 | 13+spill | 1 | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | bits=13>12 |
| `EXT.fpu_arithmetic` | `0x0406` | 1 | `FBNDXX.F_TO_EA_TO_F` | 0 | 15+spill | 1 | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | bits=15>12 |
| `EXT.fpu_arithmetic` | `0x0407` | 1 | `FBNDXX.F_TO_F_TO_F` | 0 | 13+spill | 1 | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | bits=13>12 |
| `EXT.fpu_arithmetic` | `0x0408` | 1 | `FCOPYSIGN.F_TO_F_TO_F` | 0 | 13+spill | 1 | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | bits=13>12 |
| `EXT.fpu_arithmetic` | `0x0409` | 1 | `FMADD.EA_TO_F_TO_F` | 0 | 15+spill | 1 | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | bits=15>12 |
| `EXT.fpu_arithmetic` | `0x040a` | 1 | `FMADD.F_TO_EA_TO_F` | 0 | 15+spill | 1 | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | bits=15>12 |
| `EXT.fpu_arithmetic` | `0x040b` | 1 | `FMADD.F_TO_F_TO_F` | 0 | 13+spill | 1 | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | bits=13>12 |
| `EXT.fpu_arithmetic` | `0x040c` | 1 | `FMSUB.EA_TO_F_TO_F` | 0 | 15+spill | 1 | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | bits=15>12 |
| `EXT.fpu_arithmetic` | `0x040d` | 1 | `FMSUB.F_TO_EA_TO_F` | 0 | 15+spill | 1 | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | bits=15>12 |
| `EXT.fpu_arithmetic` | `0x040e` | 1 | `FMSUB.F_TO_F_TO_F` | 0 | 13+spill | 1 | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | bits=13>12 |
| `EXT.fpu_arithmetic` | `0x040f` | 1 | `FNMADD.EA_TO_F_TO_F` | 0 | 15+spill | 1 | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | bits=15>12 |
| `EXT.fpu_arithmetic` | `0x0410..0x041f` | 16 | `FCLR.F` | 4 | 0 | 0 | f:FREG[3:0] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x0420` | 1 | `FNMADD.F_TO_EA_TO_F` | 0 | 15+spill | 1 | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | bits=15>12 |
| `EXT.fpu_arithmetic` | `0x0421` | 1 | `FNMADD.F_TO_F_TO_F` | 0 | 13+spill | 1 | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | bits=13>12 |
| `EXT.fpu_arithmetic` | `0x0422` | 1 | `FNMSUB.EA_TO_F_TO_F` | 0 | 15+spill | 1 | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | bits=15>12 |
| `EXT.fpu_arithmetic` | `0x0423` | 1 | `FNMSUB.F_TO_EA_TO_F` | 0 | 15+spill | 1 | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | bits=15>12 |
| `EXT.fpu_arithmetic` | `0x0424` | 1 | `FNMSUB.F_TO_F_TO_F` | 0 | 13+spill | 1 | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | bits=13>12 |
| `EXT.fpu_arithmetic` | `0x0425` | 1 | `FPOPM.BITMAP` | 0 | 16 | 1 | b:fbitmap16/16@payload | policy-disabled |
| `EXT.fpu_arithmetic` | `0x0426` | 1 | `FPUSHM.BITMAP` | 0 | 16 | 1 | b:fbitmap16/16@payload | policy-disabled |
| `EXT.fpu_arithmetic` | `0x0440..0x047f` | 64 | `FCLR.EA` | 6 | 0 | 0 | e:EA[5:0] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x0500..0x05ff` | 256 | `FXCHG.F_TO_F` | 8 | 0 | 0 | f:FREG[3:0], F:FREG[7:4] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x0600..0x07ff` | 512 | `FCEIL.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x0800..0x0fff` | 2048 | `FCEIL.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x1000..0x17ff` | 2048 | `FCEIL.F_TO_EA` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x1800..0x1fff` | 2048 | `FDIV.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x2000..0x21ff` | 512 | `FDIV.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x2200..0x23ff` | 512 | `FFLOOR.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x2400..0x25ff` | 512 | `FGETEXP.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x2600..0x27ff` | 512 | `FGETMAN.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x2800..0x2fff` | 2048 | `FFLOOR.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x3000..0x37ff` | 2048 | `FFLOOR.F_TO_EA` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x3800..0x3fff` | 2048 | `FGETEXP.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x4000..0x47ff` | 2048 | `FGETMAN.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x4800..0x4fff` | 2048 | `FINT.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x5000..0x57ff` | 2048 | `FINT.F_TO_EA` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x5800..0x59ff` | 512 | `FINT.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x5a00..0x5bff` | 512 | `FINTRZ.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x5c00..0x5dff` | 512 | `FMAX.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x5e00..0x5fff` | 512 | `FMIN.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x6000..0x67ff` | 2048 | `FINTRZ.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x6800..0x6fff` | 2048 | `FINTRZ.F_TO_EA` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x7000..0x77ff` | 2048 | `FMAX.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x7800..0x7fff` | 2048 | `FMIN.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x8000..0x87ff` | 2048 | `FMOD.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x8800..0x89ff` | 512 | `FMOD.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x8a00..0x8bff` | 512 | `FMUL.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x8c00..0x8dff` | 512 | `FNEG.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x8e00..0x8fff` | 512 | `FREM.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x9000..0x97ff` | 2048 | `FMUL.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0x9800..0x9fff` | 2048 | `FNEG.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xa000..0xa7ff` | 2048 | `FNEG.F_TO_EA` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xa800..0xafff` | 2048 | `FREM.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xb000..0xb7ff` | 2048 | `FROUND.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xb800..0xbfff` | 2048 | `FROUND.F_TO_EA` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xc000..0xc1ff` | 512 | `FROUND.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xc200..0xc3ff` | 512 | `FSCALE.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xc400..0xc5ff` | 512 | `FSQRT.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xc600..0xc7ff` | 512 | `FSUB.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xc800..0xcfff` | 2048 | `FSCALE.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xd000..0xd7ff` | 2048 | `FSQRT.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xd800..0xdfff` | 2048 | `FSQRT.F_TO_EA` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xe000..0xe7ff` | 2048 | `FSUB.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xe800..0xefff` | 2048 | `FTRUNC.EA_TO_F` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xf000..0xf7ff` | 2048 | `FTRUNC.F_TO_EA` | 11 | 0 | 0 | e:EA[5:0], f:FREG[9:6], z:S_D[10] | policy-disabled |
| `EXT.fpu_arithmetic` | `0xf800..0xf9ff` | 512 | `FTRUNC.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x0000..0x01ff` | 512 | `FACOS.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x0200..0x03ff` | 512 | `FASIN.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x0400..0x05ff` | 512 | `FATAN.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x0600..0x07ff` | 512 | `FATANH.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x0800..0x09ff` | 512 | `FCOS.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x0a00..0x0bff` | 512 | `FCOSH.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x0c00..0x0dff` | 512 | `FETOX.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x0e00..0x0fff` | 512 | `FETOXM1.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x1000..0x11ff` | 512 | `FLOG10.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x1200..0x13ff` | 512 | `FLOG2.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x1400..0x15ff` | 512 | `FLOGN.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x1600..0x17ff` | 512 | `FLOGNP1.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x1800..0x19ff` | 512 | `FSIN.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x1a00..0x1bff` | 512 | `FSINCOS.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x1c00..0x1dff` | 512 | `FSINH.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x1e00..0x1fff` | 512 | `FTAN.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x2000..0x21ff` | 512 | `FTANH.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x2200..0x23ff` | 512 | `FTENTOX.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |
| `EXT.fpu_transcendental` | `0x2400..0x25ff` | 512 | `FTWOTOX.F_TO_F` | 9 | 0 | 0 | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | policy-disabled |

## Compact Eviction Report

| Evicted Candidate | Reason |
| --- | --- |
| `EXTSL.D_TO_D` | compact_slots=128 |
| `SETcc.EA` | compact_slots=4096 |
| `LEA.EA_TO_A` | compact_slots=512 |
| `SEGLEA.EA_TO_A` | compact_slots=512 |
| `XCHG.D_TO_EA` | compact_slots=2048 |
| `XCHG.EA_TO_D` | compact_slots=2048 |
| `TRAPcc` | compact_slots=16 |
| `TESTCANON.EA` | compact_slots=64 |
| `CLMUL.D_TO_EA` | compact_slots=2048 |
| `CLMUL.EA_TO_D` | compact_slots=2048 |
| `CLMULH.D_TO_EA` | compact_slots=2048 |
| `CLMULH.EA_TO_D` | compact_slots=2048 |
| `CLS.EA_TO_D` | compact_slots=2048 |
| `CLZ.EA_TO_D` | compact_slots=2048 |
| `CTS.EA_TO_D` | compact_slots=2048 |
| `CTZ.EA_TO_D` | compact_slots=2048 |
| `DIVS.D_TO_EA` | compact_slots=2048 |
| `DIVS.EA_TO_D` | compact_slots=2048 |
| `DIVU.D_TO_EA` | compact_slots=2048 |
| `DIVU.EA_TO_D` | compact_slots=2048 |
| `MODS.D_TO_EA` | compact_slots=2048 |
| `MODS.EA_TO_D` | compact_slots=2048 |
| `MODU.D_TO_EA` | compact_slots=2048 |
| `MODU.EA_TO_D` | compact_slots=2048 |
| `MULHS.D_TO_EA` | compact_slots=2048 |
| `MULHS.EA_TO_D` | compact_slots=2048 |
| `MULHSU.D_TO_EA` | compact_slots=2048 |
| `MULHSU.EA_TO_D` | compact_slots=2048 |
| `MULHU.D_TO_EA` | compact_slots=2048 |
| `MULHU.EA_TO_D` | compact_slots=2048 |
| `MULS.D_TO_EA` | compact_slots=2048 |
| `MULS.EA_TO_D` | compact_slots=2048 |

## Primary Free Ranges

| Payload Range | Count |
| --- | --- |
| `0x404`..`0x407` | 4 |
| `0x444`..`0x447` | 4 |
| `0x484`..`0x487` | 4 |
| `0x4c4`..`0x4c7` | 4 |
| `0x504`..`0x507` | 4 |
| `0x544`..`0x547` | 4 |
| `0x584`..`0x587` | 4 |
| `0x5c4`..`0x5c7` | 4 |
| `0x604`..`0x607` | 4 |
| `0x644`..`0x647` | 4 |
| `0x684`..`0x687` | 4 |
| `0x6c4`..`0x6c7` | 4 |
| `0x704`..`0x707` | 4 |
| `0x744`..`0x747` | 4 |
| `0x784`..`0x787` | 4 |
| `0x7c4`..`0x7c7` | 4 |
| `0xf4e`..`0xf4e` | 1 |
| `0xf69`..`0xf6f` | 7 |
| `0xf78`..`0xffe` | 135 |
