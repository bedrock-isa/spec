# Generated Opcode Table

Generated from `isa/spec/*.yaml`. Do not edit by hand.


## Allocated Instruction Forms

This table is generated from `build/generated/allocation_plan.json` and includes instruction-catalog forms allocated by the Z3 allocator.

| Mnemonic | Form | Encoding | Words | Operands / Addressing Mode | Fields | Source |
| --- | --- | --- | --- | --- | --- | --- |
| `HALT` | `HALT` | `P:000` | 1..8 |  | none | instructions.yaml |
| `CALL` | `CALL.IMM32` | `P:001` | 3..8 | target:imm32 | none | instructions.yaml |
| `CALL` | `CALL.IMM64` | `P:002` | 5..8 | target:imm64 | none | instructions.yaml |
| `CALL` | `CALL.IMM16` | `P:003` | 2..8 | target:imm16 | none | instructions.yaml |
| `BKPT` | `BKPT` | `P:004` | 1..8 |  | none | instructions.yaml |
| `AFENCE` | `AFENCE` | `P:005` | 1..8 |  | none | instructions.yaml |
| `WFENCE` | `WFENCE` | `P:006` | 1..8 |  | none | instructions.yaml |
| `RFENCE` | `RFENCE` | `P:007` | 1..8 |  | none | instructions.yaml |
| `PUSH` | `PUSH.D` | `P:008-00f` | 1..8 | reg:DREG | d[2:0] op[11:3] | instructions.yaml |
| `AND` | `AND.IMM_TO_D` | `P:010-01f` | 2..8 | imm, dst:DREG | d[2:0] z[3] op[11:4] | instructions.yaml |
| `DEC` | `DEC.D` | `P:020-03f` | 1..8 | dst:DREG | d[2:0] s[4:3] op[11:5] | instructions.yaml |
| `EXTSW` | `EXTSW.D_TO_D` | `P:040-07f` | 1..8 | src:DREG, dst:DREG | d[2:0] D[5:3] op[11:6] | instructions.yaml |
| `ADD` | `ADD.D_TO_D` | `P:080-0ff` | 1..8 | src:DREG, dst:DREG | d[2:0] D[5:3] z[6] op[11:7] | instructions.yaml |
| `EXTSQ` | `EXTSQ.D_TO_D` | `P:100-1ff` | 1..8 | src:DREG, dst:DREG | d[2:0] D[5:3] s[7:6] op[11:8] ; exact_payloads spare=64 | instructions.yaml |
| `INC` | `INC.D` | `P:1c0-1df` | 1..8 | dst:DREG | d[2:0] s[4:3] op[11:5] | instructions.yaml |
| `ABS` | `ABS.D` | `P:1e0-1ff` | 1..8 | dst:DREG | d[2:0] s[4:3] op[11:5] | instructions.yaml |
| `EXTZQ` | `EXTZQ.D_TO_D` | `P:200-2ff` | 1..8 | src:DREG, dst:DREG | d[2:0] D[5:3] s[7:6] op[11:8] ; exact_payloads spare=64 | instructions.yaml |
| `DECN` | `DECN.D` | `P:2c0-2df` | 1..8 | dst:DREG | d[2:0] s[4:3] op[11:5] | instructions.yaml |
| `INCN` | `INCN.D` | `P:2e0-2ff` | 1..8 | dst:DREG | d[2:0] s[4:3] op[11:5] | instructions.yaml |
| `AND` | `AND.D_TO_D` | `P:300-37f` | 1..8 | src:DREG, dst:DREG | d[2:0] D[5:3] z[6] op[11:7] | instructions.yaml |
| `CMP` | `CMP.D_TO_D` | `P:380-3ff` | 1..8 | src:DREG, dst:DREG | d[2:0] D[5:3] z[6] op[11:7] | instructions.yaml |
| `ADD` | `ADD.IMM_TO_D` | `P:400-7c0` | 2..8 | imm, dst:DREG | op[5:0] d[8:6] z[9] op[11:10] ; exact_payloads spare=945 | instructions.yaml |
| `MOV` | `MOV.D_TO_EA` | `P:400-7ff` | 1..8 | src:DREG, dst:EA | e[5:0] d[8:6] z[9] op[11:10] ; exact_payloads spare=128 | instructions.yaml |
| `CMP` | `CMP.IMM_TO_D` | `P:401-7c1` | 2..8 | imm, rhs:DREG | op[5:0] d[8:6] z[9] op[11:10] ; exact_payloads spare=945 | instructions.yaml |
| `SUB` | `SUB.IMM_TO_D` | `P:402-7c2` | 2..8 | imm, dst:DREG | op[5:0] d[8:6] z[9] op[11:10] ; exact_payloads spare=945 | instructions.yaml |
| `TEST` | `TEST.IMM_TO_D` | `P:403-7c3` | 2..8 | imm, rhs:DREG | op[5:0] d[8:6] z[9] op[11:10] ; exact_payloads spare=945 | instructions.yaml |
| `MOV` | `MOV.EA_TO_D` | `P:800-bff` | 1..8 | src:EA, dst:DREG | e[5:0] d[8:6] z[9] op[11:10] | instructions.yaml |
| `OR` | `OR.D_TO_D` | `P:c00-c7f` | 1..8 | src:DREG, dst:DREG | d[2:0] D[5:3] z[6] op[11:7] | instructions.yaml |
| `SUB` | `SUB.D_TO_D` | `P:c80-cff` | 1..8 | src:DREG, dst:DREG | d[2:0] D[5:3] z[6] op[11:7] | instructions.yaml |
| `TEST` | `TEST.D_TO_D` | `P:d00-d7f` | 1..8 | src:DREG, dst:DREG | d[2:0] D[5:3] z[6] op[11:7] | instructions.yaml |
| `XOR` | `XOR.D_TO_D` | `P:d80-dff` | 1..8 | src:DREG, dst:DREG | d[2:0] D[5:3] z[6] op[11:7] | instructions.yaml |
| `EXTZL` | `EXTZL.D_TO_D` | `P:e00-e7f` | 1..8 | src:DREG, dst:DREG | d[2:0] D[5:3] s[6] op[11:7] | instructions.yaml |
| `NEG` | `NEG.D` | `P:e80-e9f` | 1..8 | dst:DREG | d[2:0] s[4:3] op[11:5] | instructions.yaml |
| `NOT` | `NOT.D` | `P:ea0-ebf` | 1..8 | dst:DREG | d[2:0] s[4:3] op[11:5] | instructions.yaml |
| `JMP` | `JMP.IMM` | `A:Jcc.IMM/T P:ec0,ed0` | 2..8 | target:relative_imm | c=0(T) z[4] op[11:5] | instructions.yaml |
| `Jcc` | `Jcc.IMM` | `P:ec0-edf` | 2..8 | cc:condition, target:relative_imm | c[3:0] z[4] op[11:5] ; exact_payloads spare=2 | instructions.yaml |
| `SYSCALL` | `SYSCALL` | `P:ec1` | 1..8 |  | none | instructions.yaml |
| `WAIT` | `WAIT` | `P:ed1` | 1..8 |  | none | instructions.yaml |
| `OR` | `OR.IMM_TO_D` | `P:ee0-eef` | 2..8 | imm, dst:DREG | d[2:0] z[3] op[11:4] | instructions.yaml |
| `XOR` | `XOR.IMM_TO_D` | `P:ef0-eff` | 2..8 | imm, dst:DREG | d[2:0] z[3] op[11:4] | instructions.yaml |
| `PUSH` | `PUSH.A` | `P:f00-f07` | 1..8 | reg:AREG | a[2:0] op[11:3] | instructions.yaml |
| `POP` | `POP.D` | `P:f08-f0f` | 1..8 | reg:DREG | d[2:0] op[11:3] | instructions.yaml |
| `POP` | `POP.A` | `P:f10-f17` | 1..8 | reg:AREG | a[2:0] op[11:3] | instructions.yaml |
| `CLR` | `CLR.A` | `P:f18-f1f` | 1..8 | dst:AREG | a[2:0] op[11:3] | instructions.yaml |
| `CLR` | `CLR.D` | `P:f20-f27` | 1..8 | dst:DREG | d[2:0] op[11:3] | instructions.yaml |
| `MOV` | `MOV.IMM_TO_A` | `P:f28-f2f` | 5..8 | src:imm64, dst:AREG | a[2:0] op[11:3] | instructions.yaml |
| `RET` | `RET` | `P:f30` | 1..8 |  | none | instructions.yaml |
| `YIELD` | `YIELD` | `P:f31` | 1..8 |  | none | instructions.yaml |
| `PUSHM` | `PUSHM.BITMAP` | `P:f32` | 2..8 | regs:bitmap16 | none | instructions.yaml |
| `POPM` | `POPM.BITMAP` | `P:f33` | 2..8 | regs:bitmap16 | none | instructions.yaml |
| `MOVSETAD` | `MOVSETAD.BITMAP` | `P:f34` | 2..8 | regs:bitmap16 | none | instructions.yaml |
| `MOVSETDA` | `MOVSETDA.BITMAP` | `P:f35` | 2..8 | regs:bitmap16 | none | instructions.yaml |
| `XCHGSETAD` | `XCHGSETAD.BITMAP` | `P:f36` | 2..8 | regs:bitmap16 | none | instructions.yaml |
| `XCHGSETDA` | `XCHGSETDA.BITMAP` | `P:f37` | 2..8 | regs:bitmap16 | none | instructions.yaml |
| `RESET` | `RESET` | `P:f38` | 1..8 |  | none | instructions.yaml |
| `SYSRET` | `SYSRET` | `P:f39` | 1..8 |  | none | instructions.yaml |
| `IRET` | `IRET` | `P:f3a` | 1..8 |  | none | instructions.yaml |
| `TRACE` | `TRACE.IMM` | `P:f3b` | 2..8 | marker:imm16 | none | instructions.yaml |
| `ABS` | `ABS.EA` | `E:f3c/0000-00ff` | 2..8 | dst:EA | e:EA[5:0], s:BWLQ[7:6] | instructions.yaml |
| `CLR` | `CLR.EA` | `E:f3c/0100-013f` | 2..8 | dst:EA | e:EA[5:0] | instructions.yaml |
| `SUM` | `SUM.BITMAP_TO_A` | `E:f3c/0140-015f` | 3..8 | regs:bitmap16, dst:AREG | a:AREG[2:0], s:BWLQ[4:3], b:bitmap16/16@payload | instructions.yaml |
| `SUM` | `SUM.BITMAP_TO_D` | `E:f3c/0160-017f` | 3..8 | regs:bitmap16, dst:DREG | d:DREG[2:0], s:BWLQ[4:3], b:bitmap16/16@payload | instructions.yaml |
| `EXTSL` | `EXTSL.D_TO_D` | `E:f3c/0180-01ff` | 2..8 | src:DREG, dst:DREG | d:DREG[2:0], D:DREG[5:3], s:BW[6] | instructions.yaml |
| `ADD` | `ADD.EA_TO_A` | `E:f3c/0200-03ff` | 2..8 | src:EA, dst:AREG | e:EA[5:0], a:AREG[8:6] | instructions.yaml |
| `CMP` | `CMP.EA_TO_A` | `E:f3c/0400-05ff` | 2..8 | lhs:EA, rhs:AREG | e:EA[5:0], a:AREG[8:6] | instructions.yaml |
| `DEC` | `DEC.EA` | `E:f3c/0600-06ff` | 2..8 | dst:EA | e:EA[5:0], s:BWLQ[7:6] | instructions.yaml |
| `DECN` | `DECN.EA` | `E:f3c/0700-07ff` | 2..8 | dst:EA | e:EA[5:0], s:BWLQ[7:6] | instructions.yaml |
| `AND` | `AND.EA_TO_D` | `E:f3c/0800-0fff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `CMP` | `CMP.D_TO_EA` | `E:f3c/1000-17ff` | 2..8 | lhs:DREG, rhs:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `CMP` | `CMP.EA_TO_D` | `E:f3c/1800-1fff` | 2..8 | lhs:EA, rhs:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `EXTSL` | `EXTSL.D_TO_EA` | `E:f3c/2000-23ff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BW[9] | instructions.yaml |
| `EXTSL` | `EXTSL.EA_TO_D` | `E:f3c/2400-27ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BW[9] | instructions.yaml |
| `EXTSQ` | `EXTSQ.D_TO_EA` | `E:f3c/2800-2fff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWL[10:9] | instructions.yaml |
| `EXTSQ` | `EXTSQ.EA_TO_D` | `E:f3c/3000-37ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWL[10:9] | instructions.yaml |
| `EXTSW` | `EXTSW.D_TO_EA` | `E:f3c/3800-39ff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6] | instructions.yaml |
| `EXTSW` | `EXTSW.EA_TO_D` | `E:f3c/3a00-3bff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6] | instructions.yaml |
| `EXTZL` | `EXTZL.D_TO_EA` | `E:f3c/3c00-3fff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BW[9] | instructions.yaml |
| `EXTZL` | `EXTZL.EA_TO_D` | `E:f3c/4000-43ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BW[9] | instructions.yaml |
| `INC` | `INC.EA` | `E:f3c/4400-44ff` | 2..8 | dst:EA | e:EA[5:0], s:BWLQ[7:6] | instructions.yaml |
| `INCN` | `INCN.EA` | `E:f3c/4500-45ff` | 2..8 | dst:EA | e:EA[5:0], s:BWLQ[7:6] | instructions.yaml |
| `NEG` | `NEG.EA` | `E:f3c/4600-46ff` | 2..8 | dst:EA | e:EA[5:0], s:BWLQ[7:6] | instructions.yaml |
| `NOT` | `NOT.EA` | `E:f3c/4700-47ff` | 2..8 | dst:EA | e:EA[5:0], s:BWLQ[7:6] | instructions.yaml |
| `EXTZQ` | `EXTZQ.D_TO_EA` | `E:f3c/4800-4fff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWL[10:9] | instructions.yaml |
| `EXTZQ` | `EXTZQ.EA_TO_D` | `E:f3c/5000-57ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWL[10:9] | instructions.yaml |
| `MAXS` | `MAXS.D_TO_EA` | `E:f3c/5800-5fff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MAXS` | `MAXS.EA_TO_D` | `E:f3c/6000-67ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MAXU` | `MAXU.D_TO_EA` | `E:f3c/6800-6fff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MAXU` | `MAXU.EA_TO_D` | `E:f3c/7000-77ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MINS` | `MINS.D_TO_EA` | `E:f3c/7800-7fff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MINS` | `MINS.EA_TO_D` | `E:f3c/8000-87ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MINU` | `MINU.D_TO_EA` | `E:f3c/8800-8fff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MINU` | `MINU.EA_TO_D` | `E:f3c/9000-97ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `OR` | `OR.D_TO_EA` | `E:f3c/9800-9fff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `OR` | `OR.EA_TO_D` | `E:f3c/a000-a7ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `REVBYTE` | `REVBYTE.D_TO_D` | `E:f3c/a800-a8ff` | 2..8 | src:DREG, dst:DREG | d:DREG[2:0], D:DREG[5:3], s:BWLQ[7:6] | instructions.yaml |
| `SUB` | `SUB.EA_TO_A` | `E:f3c/aa00-abff` | 2..8 | src:EA, dst:AREG | e:EA[5:0], a:AREG[8:6] | instructions.yaml |
| `REVBYTE` | `REVBYTE.D_TO_EA` | `E:f3c/b000-b7ff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `REVBYTE` | `REVBYTE.EA_TO_D` | `E:f3c/b800-bfff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `SBB` | `SBB.D_TO_EA` | `E:f3c/c000-c7ff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `SBB` | `SBB.EA_TO_D` | `E:f3c/c800-cfff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `SUB` | `SUB.D_TO_EA` | `E:f3c/d000-d7ff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `SUB` | `SUB.EA_TO_D` | `E:f3c/d800-dfff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `TEST` | `TEST.D_TO_EA` | `E:f3c/e000-e7ff` | 2..8 | lhs:DREG, rhs:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `TEST` | `TEST.EA_TO_D` | `E:f3c/e800-efff` | 2..8 | lhs:EA, rhs:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `XOR` | `XOR.D_TO_EA` | `E:f3c/f000-f7ff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `XOR` | `XOR.EA_TO_D` | `E:f3c/f800-ffff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `ADC` | `ADC.D_TO_EA` | `E:f3d/0000-07ff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `ADC` | `ADC.EA_TO_D` | `E:f3d/0800-0fff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `ADD` | `ADD.D_TO_EA` | `E:f3d/1000-17ff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `ADD` | `ADD.EA_TO_D` | `E:f3d/1800-1fff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `AND` | `AND.D_TO_EA` | `E:f3d/2000-27ff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `ADC` | `ADC.IMM_TO_EA` | `E:f3e/0000-3fff` | 2..8 | imm:imm6, dst:EA | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | instructions.yaml |
| `ADD` | `ADD.IMM_TO_EA` | `E:f3e/4000-7fff` | 2..8 | imm:imm6, dst:EA | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | instructions.yaml |
| `SBB` | `SBB.IMM_TO_EA` | `E:f3e/8000-bfff` | 2..8 | imm:imm6, dst:EA | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | instructions.yaml |
| `SUB` | `SUB.IMM_TO_EA` | `E:f3e/c000-ffff` | 2..8 | imm:imm6, dst:EA | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | instructions.yaml |
| `AND` | `AND.IMM_TO_EA` | `E:f3f/0000-3fff` | 2..8 | imm:imm6, dst:EA | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | instructions.yaml |
| `OR` | `OR.IMM_TO_EA` | `E:f3f/4000-7fff` | 2..8 | imm:imm6, dst:EA | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | instructions.yaml |
| `TEST` | `TEST.IMM_TO_EA` | `E:f3f/8000-bfff` | 2..8 | imm:imm6, rhs:EA | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | instructions.yaml |
| `XOR` | `XOR.IMM_TO_EA` | `E:f3f/c000-ffff` | 2..8 | imm:imm6, dst:EA | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | instructions.yaml |
| `CMP` | `CMP.EA_TO_EA` | `E:f40/0000-3fff` | 2..8 | lhs:EA, rhs:EA | e:EA[5:0], E:EA[11:6], s:BWLQ[13:12] | instructions.yaml |
| `CMP` | `CMP.IMM_TO_EA` | `E:f40/4000-7fff` | 2..8 | imm:imm6, rhs:EA | e:EA[5:0], s:BWLQ[7:6], i:IMM6[13:8] | instructions.yaml |
| `EXTSL` | `EXTSL.EA_TO_EA` | `E:f41/0000-1fff` | 2..8 | src:EA, dst:EA | e:EA[5:0], E:EA[11:6], s:BW[12] | instructions.yaml |
| `EXTSW` | `EXTSW.EA_TO_EA` | `E:f41/2000-2fff` | 2..8 | src:EA, dst:EA | e:EA[5:0], E:EA[11:6] | instructions.yaml |
| `EXTZW` | `EXTZW.EA_TO_EA` | `E:f41/3000-3fff` | 2..8 | src:EA, dst:EA | e:EA[5:0], E:EA[11:6] | instructions.yaml |
| `EXTSQ` | `EXTSQ.EA_TO_EA` | `E:f41/4000-7fff` | 2..8 | src:EA, dst:EA | e:EA[5:0], E:EA[11:6], s:BWL[13:12] | instructions.yaml |
| `EXTZL` | `EXTZL.EA_TO_EA` | `E:f41/8000-9fff` | 2..8 | src:EA, dst:EA | e:EA[5:0], E:EA[11:6], s:BW[12] | instructions.yaml |
| `EXTZQ` | `EXTZQ.EA_TO_EA` | `E:f41/c000-ffff` | 2..8 | src:EA, dst:EA | e:EA[5:0], E:EA[11:6], s:BWL[13:12] | instructions.yaml |
| `BNDSII` | `BNDSII.D_TO_EA_TO_D` | `E:f42/0000-3fff` | 2..8 | lo:DREG, value:EA, hi:DREG | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | instructions.yaml |
| `BNDSIX` | `BNDSIX.D_TO_EA_TO_D` | `E:f42/4000-7fff` | 2..8 | lo:DREG, value:EA, hi:DREG | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | instructions.yaml |
| `BNDSXI` | `BNDSXI.D_TO_EA_TO_D` | `E:f42/8000-bfff` | 2..8 | lo:DREG, value:EA, hi:DREG | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | instructions.yaml |
| `BNDSXX` | `BNDSXX.D_TO_EA_TO_D` | `E:f42/c000-ffff` | 2..8 | lo:DREG, value:EA, hi:DREG | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | instructions.yaml |
| `BNDUII` | `BNDUII.D_TO_EA_TO_D` | `E:f43/0000-3fff` | 2..8 | lo:DREG, value:EA, hi:DREG | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | instructions.yaml |
| `BNDUIX` | `BNDUIX.D_TO_EA_TO_D` | `E:f43/4000-7fff` | 2..8 | lo:DREG, value:EA, hi:DREG | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | instructions.yaml |
| `BNDUXI` | `BNDUXI.D_TO_EA_TO_D` | `E:f43/8000-bfff` | 2..8 | lo:DREG, value:EA, hi:DREG | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | instructions.yaml |
| `BNDUXX` | `BNDUXX.D_TO_EA_TO_D` | `E:f43/c000-ffff` | 2..8 | lo:DREG, value:EA, hi:DREG | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | instructions.yaml |
| `CLMUL` | `CLMUL.D_TO_EA` | `E:f44/0000-07ff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `CLMUL` | `CLMUL.EA_TO_D` | `E:f44/0800-0fff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `CLMULH` | `CLMULH.D_TO_EA` | `E:f44/1000-17ff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `CLMULH` | `CLMULH.EA_TO_D` | `E:f44/1800-1fff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `DIVMODS` | `DIVMODS.EA_TO_D_TO_D` | `E:f44/2000` | 3..8 | src:EA, quotient:DREG, remainder:DREG | e:EA/6@payload, d:DREG/3@payload, D:DREG/3@payload, s:BWLQ/2@payload | instructions.yaml |
| `DIVS` | `DIVS.D_TO_EA` | `E:f44/2800-2fff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `DIVS` | `DIVS.EA_TO_D` | `E:f44/3000-37ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `DIVU` | `DIVU.D_TO_EA` | `E:f44/3800-3fff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `DIVMODU` | `DIVMODU.EA_TO_D_TO_D` | `E:f44/4000-7fff` | 2..8 | src:EA, quotient:DREG, remainder:DREG | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | instructions.yaml |
| `DIVU` | `DIVU.EA_TO_D` | `E:f44/8000-87ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MODS` | `MODS.D_TO_EA` | `E:f44/8800-8fff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MODS` | `MODS.EA_TO_D` | `E:f44/9000-97ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MODU` | `MODU.D_TO_EA` | `E:f44/9800-9fff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MODU` | `MODU.EA_TO_D` | `E:f44/a000-a7ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MULHS` | `MULHS.D_TO_EA` | `E:f44/a800-afff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MULHS` | `MULHS.EA_TO_D` | `E:f44/b000-b7ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MULHSU` | `MULHSU.D_TO_EA` | `E:f44/b800-bfff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MULHSU` | `MULHSU.EA_TO_D` | `E:f44/c000-c7ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MULHU` | `MULHU.D_TO_EA` | `E:f44/c800-cfff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MULHU` | `MULHU.EA_TO_D` | `E:f44/d000-d7ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MULS` | `MULS.D_TO_EA` | `E:f44/d800-dfff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MULS` | `MULS.EA_TO_D` | `E:f44/e000-e7ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MULU` | `MULU.D_TO_EA` | `E:f44/e800-efff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MULU` | `MULU.EA_TO_D` | `E:f44/f000-f7ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MADD` | `MADD.EA_TO_D_TO_D` | `E:f45/0000-3fff` | 2..8 | src:EA, multiplier:DREG, acc:DREG | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | instructions.yaml |
| `MSUB` | `MSUB.EA_TO_D_TO_D` | `E:f45/4000-7fff` | 2..8 | src:EA, multiplier:DREG, acc:DREG | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], s:BWLQ[13:12] | instructions.yaml |
| `BCHG` | `BCHG.D_TO_D` | `E:f46/0000-00ff` | 2..8 | bit_index:DREG, dst:DREG | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | instructions.yaml |
| `BCLR` | `BCLR.D_TO_D` | `E:f46/0100-01ff` | 2..8 | bit_index:DREG, dst:DREG | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | instructions.yaml |
| `BSET` | `BSET.D_TO_D` | `E:f46/0200-02ff` | 2..8 | bit_index:DREG, dst:DREG | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | instructions.yaml |
| `BTEST` | `BTEST.D_TO_D` | `E:f46/0300-03ff` | 2..8 | bit_index:DREG, dst:DREG | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | instructions.yaml |
| `PARITY` | `PARITY.EA` | `E:f46/0400-04ff` | 2..8 | src:EA | e:EA[5:0], s:BWLQ[7:6] | instructions.yaml |
| `RCL` | `RCL.D_TO_D` | `E:f46/0500-05ff` | 2..8 | count:DREG, dst:DREG | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | instructions.yaml |
| `RCR` | `RCR.D_TO_D` | `E:f46/0600-06ff` | 2..8 | count:DREG, dst:DREG | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | instructions.yaml |
| `REVBIT` | `REVBIT.D_TO_D` | `E:f46/0700-07ff` | 2..8 | src:DREG, dst:DREG | d:DREG[2:0], D:DREG[5:3], s:BWLQ[7:6] | instructions.yaml |
| `BCHG` | `BCHG.D_TO_EA` | `E:f46/0800-0fff` | 2..8 | bit_index:DREG, dst:EA | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `BCLR` | `BCLR.D_TO_EA` | `E:f46/1000-17ff` | 2..8 | bit_index:DREG, dst:EA | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `BSET` | `BSET.D_TO_EA` | `E:f46/1800-1fff` | 2..8 | bit_index:DREG, dst:EA | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `BTEST` | `BTEST.D_TO_EA` | `E:f46/2000-27ff` | 2..8 | bit_index:DREG, dst:EA | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `CLS` | `CLS.EA_TO_D` | `E:f46/2800-2fff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `CLZ` | `CLZ.EA_TO_D` | `E:f46/3000-37ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `CTS` | `CTS.EA_TO_D` | `E:f46/3800-3fff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `CTZ` | `CTZ.EA_TO_D` | `E:f46/4000-47ff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `POPCNT` | `POPCNT.EA_TO_D` | `E:f46/4800-4fff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `RCL` | `RCL.D_TO_EA` | `E:f46/5000-57ff` | 2..8 | count:DREG, dst:EA | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `RCR` | `RCR.D_TO_EA` | `E:f46/5800-5fff` | 2..8 | count:DREG, dst:EA | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `REVBIT` | `REVBIT.D_TO_EA` | `E:f46/6000-67ff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `REVBIT` | `REVBIT.EA_TO_D` | `E:f46/6800-6fff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `ROL` | `ROL.D_TO_D` | `E:f46/7000-70ff` | 2..8 | count:DREG, dst:DREG | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | instructions.yaml |
| `ROR` | `ROR.D_TO_D` | `E:f46/7100-71ff` | 2..8 | count:DREG, dst:DREG | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | instructions.yaml |
| `SAR` | `SAR.D_TO_D` | `E:f46/7200-72ff` | 2..8 | count:DREG, dst:DREG | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | instructions.yaml |
| `SHL` | `SHL.D_TO_D` | `E:f46/7300-73ff` | 2..8 | count:DREG, dst:DREG | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | instructions.yaml |
| `SHR` | `SHR.D_TO_D` | `E:f46/7400-74ff` | 2..8 | count:DREG, dst:DREG | n:DREG[2:0], d:DREG[5:3], s:BWLQ[7:6] | instructions.yaml |
| `ROL` | `ROL.D_TO_EA` | `E:f46/7800-7fff` | 2..8 | count:DREG, dst:EA | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `ROR` | `ROR.D_TO_EA` | `E:f46/8000-87ff` | 2..8 | count:DREG, dst:EA | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `SAR` | `SAR.D_TO_EA` | `E:f46/8800-8fff` | 2..8 | count:DREG, dst:EA | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `SHL` | `SHL.D_TO_EA` | `E:f46/9000-97ff` | 2..8 | count:DREG, dst:EA | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `SHR` | `SHR.D_TO_EA` | `E:f46/9800-9fff` | 2..8 | count:DREG, dst:EA | e:EA[5:0], n:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `BCHG` | `BCHG.I6_TO_EA` | `E:f47/0000-3fff` | 2..8 | bit_index:imm6, dst:EA | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:bit_group=BCHG[15:14] | instructions.yaml |
| `BCLR` | `BCLR.I6_TO_EA` | `E:f47/4000-7fff` | 2..8 | bit_index:imm6, dst:EA | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:bit_group=BCLR[15:14] | instructions.yaml |
| `BSET` | `BSET.I6_TO_EA` | `E:f47/8000-bfff` | 2..8 | bit_index:imm6, dst:EA | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:bit_group=BSET[15:14] | instructions.yaml |
| `BTEST` | `BTEST.I6_TO_EA` | `E:f47/c000-ffff` | 2..8 | bit_index:imm6, dst:EA | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:bit_group=BTEST[15:14] | instructions.yaml |
| `RCL` | `RCL.I6_TO_EA` | `E:f48/0000-3fff` | 2..8 | count:imm6, dst:EA | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:rotate_group=RCL[15:14] | instructions.yaml |
| `RCR` | `RCR.I6_TO_EA` | `E:f48/4000-7fff` | 2..8 | count:imm6, dst:EA | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:rotate_group=RCR[15:14] | instructions.yaml |
| `ROL` | `ROL.I6_TO_EA` | `E:f48/8000-bfff` | 2..8 | count:imm6, dst:EA | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:rotate_group=ROL[15:14] | instructions.yaml |
| `ROR` | `ROR.I6_TO_EA` | `E:f48/c000-ffff` | 2..8 | count:imm6, dst:EA | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:rotate_group=ROR[15:14] | instructions.yaml |
| `SHL` | `SHL.I6_TO_EA` | `E:f49/0000-3fff` | 2..8 | count:imm6, dst:EA | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:shift_group=SHL[15:14] | instructions.yaml |
| `SHR` | `SHR.I6_TO_EA` | `E:f49/4000-7fff` | 2..8 | count:imm6, dst:EA | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:shift_group=SHR[15:14] | instructions.yaml |
| `SAR` | `SAR.I6_TO_EA` | `E:f49/8000-bfff` | 2..8 | count:imm6, dst:EA | e:EA[5:0], n:selector6[11:6], s:BWLQ[13:12], o:shift_group=SAR[15:14] | instructions.yaml |
| `MOV` | `MOV.D_TO_EA_WIDE` | `E:f4a/0000-07ff` | 2..8 | src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MOV` | `MOV.EA_TO_D_WIDE` | `E:f4a/0800-0fff` | 2..8 | src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `XCHG` | `XCHG.D_TO_EA` | `E:f4a/1000-17ff` | 2..8 | lhs:DREG, rhs:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `XCHG` | `XCHG.EA_TO_D` | `E:f4a/1800-1fff` | 2..8 | lhs:EA, rhs:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9] | instructions.yaml |
| `MOV` | `MOV.EA_TO_EA` | `E:f4a/4000-7fff` | 2..8 | src:EA, dst:EA | e:EA[5:0], E:EA[11:6], s:BWLQ[13:12] | instructions.yaml |
| `GETDB` | `GETDB.D` | `E:f4b/0000-0007` | 2..8 | dst:DREG | d:DREG[2:0] | instructions.yaml |
| `SELDB` | `SELDB.D` | `E:f4b/0008-000f` | 2..8 | selector:DREG | d:DREG[2:0] | instructions.yaml |
| `MOVSETAD` | `MOVSETAD.DB_TO_BITMAP` | `E:f4b/0010-001f` | 3..8 | src_bank:DBANK, regs:bitmap16 | k:DBANK[3:0], b:bitmap16/16@payload | instructions.yaml |
| `MOVSETDA` | `MOVSETDA.DB_TO_BITMAP` | `E:f4b/0020-002f` | 3..8 | dst_bank:DBANK, regs:bitmap16 | k:DBANK[3:0], b:bitmap16/16@payload | instructions.yaml |
| `SELDB` | `SELDB.DB` | `E:f4b/0030-003f` | 2..8 | selector:DBANK | k:DBANK[3:0] | instructions.yaml |
| `XCHGSETAD` | `XCHGSETAD.DB_TO_BITMAP` | `E:f4b/0040-004f` | 3..8 | bank:DBANK, regs:bitmap16 | k:DBANK[3:0], b:bitmap16/16@payload | instructions.yaml |
| `XCHGSETDA` | `XCHGSETDA.DB_TO_BITMAP` | `E:f4b/0050-005f` | 3..8 | bank:DBANK, regs:bitmap16 | k:DBANK[3:0], b:bitmap16/16@payload | instructions.yaml |
| `MOVSETDD` | `MOVSETDD.DB_TO_DB_TO_BITMAP` | `E:f4b/0100-01ff` | 3..8 | dst_bank:DBANK, src_bank:DBANK, regs:bitmap16 | k:DBANK[3:0], K:DBANK[7:4], b:bitmap16/16@payload | instructions.yaml |
| `XCHGSETDD` | `XCHGSETDD.DB_TO_DB_TO_BITMAP` | `E:f4b/0200-02ff` | 3..8 | bank_a:DBANK, bank_b:DBANK, regs:bitmap16 | k:DBANK[3:0], K:DBANK[7:4], b:bitmap16/16@payload | instructions.yaml |
| `LEA` | `LEA.EA_TO_A` | `E:f4c/0000-01ff` | 2..8 | src:EA, dst:AREG | e:EA[5:0], a:AREG[8:6] | instructions.yaml |
| `SEGLEA` | `SEGLEA.EA_TO_A` | `E:f4c/0200-03ff` | 2..8 | src:EA, dst:AREG | e:EA[5:0], a:AREG[8:6] | instructions.yaml |
| `TESTCANON` | `TESTCANON.EA` | `E:f4c/0400-043f` | 2..8 | src:EA | e:EA[5:0] | instructions.yaml |
| `CALL` | `CALL.EA` | `E:f4d/0000-003f` | 2..8 | target:EA | e:EA[5:0] | instructions.yaml |
| `LRET` | `LRET` | `E:f4d/0040` | 2..8 |  | none | instructions.yaml |
| `LCALL` | `LCALL.D_TO_EA` | `E:f4d/0200-03ff` | 2..8 | new_cs:DREG, target:EA | e:EA[5:0], d:DREG[8:6] | instructions.yaml |
| `LJMP` | `LJMP.D_TO_EA` | `E:f4d/0400-05ff` | 2..8 | new_cs:DREG, target:EA | e:EA[5:0], d:DREG[8:6] | instructions.yaml |
| `NOP` | `NOP` | `P:f4f` | 1..8 |  | none | instructions.yaml |
| `DJcc` | `DJcc.D_TO_EA` | `E:f50-f5f/0000-07ff` | 2..8 | cc:condition, counter:DREG, target:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9], c:condition/4@root | instructions.yaml |
| `FMOVcc` | `FMOVcc.F_TO_F` | `E:f50-f5f/0800-08ff` | 2..8 | cc:condition, src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], c:condition/4@root | instructions.yaml |
| `TRAP` | `TRAP` | `A:TRAPcc/T E:f50/0900` | 2..8 |  | c=0(T)@root | instructions.yaml |
| `TRAPcc` | `TRAPcc` | `E:f50-f5f/0900` | 2..8 | cc:condition | c:condition/4@root | instructions.yaml |
| `JMP` | `JMP.EA` | `A:Jcc.EA/T E:f50/0980-09ff` | 2..8 | target:EA | c=0(T)@root, z:WL/1@ext, e:EA/6@ext | instructions.yaml |
| `Jcc` | `Jcc.EA` | `E:f50-f5f/0980-09ff` | 2..8 | cc:condition, target:EA | e:EA[5:0], z:WL[6], c:condition/4@root | instructions.yaml |
| `SETcc` | `SETcc.EA` | `E:f50-f5f/0a00-0aff` | 2..8 | cc:condition, dst:EA | e:EA[5:0], s:BWLQ[7:6], c:condition/4@root | instructions.yaml |
| `MOVcc` | `MOVcc.A_TO_EA` | `E:f50-f5f/1000-17ff` | 2..8 | cc:condition, src:AREG, dst:EA | e:EA[5:0], a:AREG[8:6], s:BWLQ[10:9], c:condition/4@root | instructions.yaml |
| `MOVcc` | `MOVcc.D_TO_EA` | `E:f50-f5f/1800-1fff` | 2..8 | cc:condition, src:DREG, dst:EA | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9], c:condition/4@root | instructions.yaml |
| `IJcc` | `IJcc.D_TO_D_TO_EA` | `E:f50-f5f/2000-3fff` | 2..8 | cc:condition, index:DREG, bound:DREG, target:EA | e:EA[5:0], d:DREG[8:6], D:DREG[11:9], z:LQ[12], c:condition/4@root | instructions.yaml |
| `MOVcc` | `MOVcc.EA_TO_A` | `E:f50-f5f/4000-47ff` | 2..8 | cc:condition, src:EA, dst:AREG | e:EA[5:0], a:AREG[8:6], s:BWLQ[10:9], c:condition/4@root | instructions.yaml |
| `MOVcc` | `MOVcc.EA_TO_D` | `E:f50-f5f/4800-4fff` | 2..8 | cc:condition, src:EA, dst:DREG | e:EA[5:0], d:DREG[8:6], s:BWLQ[10:9], c:condition/4@root | instructions.yaml |
| `FMOVcc` | `FMOVcc.EA_TO_F` | `E:f50-f5f/5000-57ff` | 2..8 | cc:condition, src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10], c:condition/4@root | instructions.yaml |
| `FMOVcc` | `FMOVcc.F_TO_EA` | `E:f50-f5f/5800-5fff` | 2..8 | cc:condition, src:FREG, dst:EA | e:EA[5:0], f:FREG[9:6], z:S_D[10], c:condition/4@root | instructions.yaml |
| `CMPXCHG` | `CMPXCHG.D_TO_D_TO_EA` | `E:f60/0000-0003` | 3..8 | order:memory_order, expected:DREG, desired:DREG, memory:EA | s:BWLQ[1:0], o:memory_order/3@payload, e:EA/6@payload, d:DREG/3@payload, D:DREG/3@payload | instructions.yaml |
| `FETCHADD` | `FETCHADD.D_TO_EA` | `E:f60/0004` | 3..8 | order:memory_order, src:DREG, memory:EA | o:memory_order/3@payload, e:EA/6@payload, d:DREG/3@payload, s:BWLQ/2@payload | instructions.yaml |
| `FETCHAND` | `FETCHAND.D_TO_EA` | `E:f60/0005` | 3..8 | order:memory_order, src:DREG, memory:EA | o:memory_order/3@payload, e:EA/6@payload, d:DREG/3@payload, s:BWLQ/2@payload | instructions.yaml |
| `FETCHOR` | `FETCHOR.D_TO_EA` | `E:f60/0006` | 3..8 | order:memory_order, src:DREG, memory:EA | o:memory_order/3@payload, e:EA/6@payload, d:DREG/3@payload, s:BWLQ/2@payload | instructions.yaml |
| `FETCHSUB` | `FETCHSUB.D_TO_EA` | `E:f60/0007` | 3..8 | order:memory_order, src:DREG, memory:EA | o:memory_order/3@payload, e:EA/6@payload, d:DREG/3@payload, s:BWLQ/2@payload | instructions.yaml |
| `FETCHXOR` | `FETCHXOR.D_TO_EA` | `E:f60/0008` | 3..8 | order:memory_order, src:DREG, memory:EA | o:memory_order/3@payload, e:EA/6@payload, d:DREG/3@payload, s:BWLQ/2@payload | instructions.yaml |
| `PREFETCH` | `PREFETCH.EA` | `E:f61/0000-003f` | 2..8 | src:EA | e:EA[5:0] | instructions.yaml |
| `INVTLB` | `INVTLB` | `E:f62/0000` | 2..8 |  | none | instructions.yaml |
| `INVASID` | `INVASID.IMM` | `E:f62/0001` | 3..8 | asid:IMM16 | i:IMM16/16@payload | instructions.yaml |
| `SWPT` | `SWPT.D` | `E:f62/0008-000f` | 2..8 | new_ptcr:DREG | d:DREG[2:0] | instructions.yaml |
| `RDPTC` | `RDPTC.D` | `E:f62/0010-0017` | 2..8 | dst:DREG | d:DREG[2:0] | instructions.yaml |
| `INVPAGE` | `INVPAGE.EA` | `E:f62/0040-007f` | 2..8 | page:EA | e:EA[5:0] | instructions.yaml |
| `SWPTA` | `SWPTA.D_TO_D` | `E:f62/0080-00bf` | 2..8 | new_ptcr:DREG, asid:DREG | d:DREG[2:0], D:DREG[5:3] | instructions.yaml |
| `INVDCACHE` | `INVDCACHE.EA` | `E:f62/00c0-00ff` | 2..8 | target:EA | e:EA[5:0] | instructions.yaml |
| `WRBKDCACHE` | `WRBKDCACHE.EA` | `E:f62/0100-013f` | 2..8 | target:EA | e:EA[5:0] | instructions.yaml |
| `FLSHDCACHE` | `FLSHDCACHE.EA` | `E:f62/0140-017f` | 2..8 | target:EA | e:EA[5:0] | instructions.yaml |
| `INVICACHE` | `INVICACHE.EA` | `E:f62/0180-01bf` | 2..8 | target:EA | e:EA[5:0] | instructions.yaml |
| `SYNCCACHE` | `SYNCCACHE.EA` | `E:f62/01c0-01ff` | 2..8 | target:EA | e:EA[5:0] | instructions.yaml |
| `PTATTR` | `PTATTR.EA` | `E:f62/0200-023f` | 2..8 | src:EA, outputs | e:EA[5:0] | instructions.yaml |
| `PTQUERY` | `PTQUERY.EA` | `E:f62/0240-027f` | 2..8 | src:EA, outputs | e:EA[5:0] | instructions.yaml |
| `VTOP` | `VTOP.EA` | `E:f62/0280-02bf` | 2..8 | src:EA, outputs | e:EA[5:0] | instructions.yaml |
| `RDCR` | `RDCR.D` | `E:f63/0000-0007` | 3..8 | cr:CR, dst:DREG | d:DREG[2:0], i:CR/16@payload | instructions.yaml |
| `WRCR` | `WRCR.D` | `E:f63/0008-000f` | 3..8 | src:DREG, cr:CR | d:DREG[2:0], i:CR/16@payload | instructions.yaml |
| `RDFLAGS` | `RDFLAGS.D` | `E:f63/0010-0017` | 2..8 | dst:DREG | d:DREG[2:0] | instructions.yaml |
| `WRFLAGS` | `WRFLAGS.D` | `E:f63/0018-001f` | 2..8 | src:DREG | d:DREG[2:0] | instructions.yaml |
| `RDSTATUS` | `RDSTATUS.D` | `E:f63/0020-0027` | 2..8 | dst:DREG | d:DREG[2:0] | instructions.yaml |
| `WRSTATUS` | `WRSTATUS.D` | `E:f63/0028-002f` | 2..8 | src:DREG | d:DREG[2:0] | instructions.yaml |
| `CPUID` | `CPUID.D` | `E:f63/0030-0037` | 2..8 | reg:DREG | d:DREG[2:0] | instructions.yaml |
| `RDFSTATUS` | `RDFSTATUS.D` | `E:f63/0038-003f` | 2..8 | dst:DREG | d:DREG[2:0] | instructions.yaml |
| `RDSEG` | `RDSEG.S_TO_D` | `E:f63/0040-007f` | 2..8 | seg:SREG, dst:DREG | g:SREG[2:0], d:DREG[5:3] | instructions.yaml |
| `WRSEG` | `WRSEG.D_TO_S` | `E:f63/0080-00bf` | 2..8 | src:DREG, seg:SREG | d:DREG[2:0], g:SREG[5:3] | instructions.yaml |
| `SAVE` | `SAVE.EA` | `E:f63/00c0-00ff` | 2..8 | memory:EA | e:EA[5:0] | instructions.yaml |
| `RESTORE` | `RESTORE.EA` | `E:f63/0100-013f` | 2..8 | memory:EA | e:EA[5:0] | instructions.yaml |
| `RDPMC` | `RDPMC.IMM_TO_D` | `E:f63/0140-0147` | 3..8 | counter_id:IMM16, dst:DREG | d:DREG[2:0], i:IMM16/16@payload | instructions.yaml |
| `WRFSTATUS` | `WRFSTATUS.D` | `E:f63/0148-014f` | 2..8 | src:DREG | d:DREG[2:0] | instructions.yaml |
| `ENCINST` | `ENCINST.EA` | `E:f64/0000-003f` | 2..8 | dst:EA | e:EA[5:0] | instructions.yaml |
| `FCMP` | `FCMP.F_TO_F` | `E:f65/0000-01ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FTEST` | `FTEST.F` | `E:f65/0200-021f` | 2..8 | src:FREG | f:FREG[3:0], z:S_D[4] | instructions.yaml |
| `FMOVCR` | `FMOVCR.IMM_TO_F` | `E:f65/0220-022f` | 3..8 | constant_id:IMM16, dst:FREG | f:FREG[3:0], i:IMM16/16@payload | instructions.yaml |
| `FCVT` | `FCVT.D_TO_F` | `E:f65/0280-02ff` | 2..8 | src:DREG, dst:FREG | d:DREG[2:0], f:FREG[6:3] | instructions.yaml |
| `FCLASS` | `FCLASS.F_TO_D` | `E:f65/0300-03ff` | 2..8 | src:FREG, dst:DREG | d:DREG[2:0], f:FREG[6:3], z:S_D[7] | instructions.yaml |
| `FMOV` | `FMOV.F_TO_F` | `E:f65/0400-05ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FCVT` | `FCVT.F_TO_D` | `E:f65/0600-067f` | 2..8 | src:FREG, dst:DREG | d:DREG[2:0], f:FREG[6:3] | instructions.yaml |
| `FCVTU` | `FCVTU.D_TO_F` | `E:f65/0680-06ff` | 2..8 | src:DREG, dst:FREG | d:DREG[2:0], f:FREG[6:3] | instructions.yaml |
| `FCVT` | `FCVT.F_TO_F` | `E:f65/0700-07ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4] | instructions.yaml |
| `FCMP` | `FCMP.EA_TO_F` | `E:f65/0800-0fff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FTEST` | `FTEST.EA` | `E:f65/1000-107f` | 2..8 | src:EA | e:EA[5:0], z:S_D[6] | instructions.yaml |
| `FCVTU` | `FCVTU.F_TO_D` | `E:f65/1080-10ff` | 2..8 | src:FREG, dst:DREG | d:DREG[2:0], f:FREG[6:3] | instructions.yaml |
| `FCVTU` | `FCVTU.F_TO_F` | `E:f65/1100-11ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4] | instructions.yaml |
| `FMOV` | `FMOV.EA_TO_F` | `E:f65/1800-1fff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FMOV` | `FMOV.F_TO_EA` | `E:f65/2000-27ff` | 2..8 | src:FREG, dst:EA | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FABS` | `FABS.EA_TO_F` | `E:f66/0000-07ff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FABS` | `FABS.F_TO_EA` | `E:f66/0800-0fff` | 2..8 | src:FREG, dst:EA | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FADD` | `FADD.EA_TO_F` | `E:f66/1000-17ff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FABS` | `FABS.F_TO_F` | `E:f67/0000-01ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FADD` | `FADD.F_TO_F` | `E:f67/0200-03ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FBNDII` | `FBNDII.F_TO_EA_TO_F` | `E:f67/0400` | 3..8 | lo:FREG, value:EA, hi:FREG | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FBNDII` | `FBNDII.F_TO_F_TO_F` | `E:f67/0401` | 3..8 | lo:FREG, value:FREG, hi:FREG | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FBNDIX` | `FBNDIX.F_TO_EA_TO_F` | `E:f67/0402` | 3..8 | lo:FREG, value:EA, hi:FREG | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FBNDIX` | `FBNDIX.F_TO_F_TO_F` | `E:f67/0403` | 3..8 | lo:FREG, value:FREG, hi:FREG | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FBNDXI` | `FBNDXI.F_TO_EA_TO_F` | `E:f67/0404` | 3..8 | lo:FREG, value:EA, hi:FREG | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FBNDXI` | `FBNDXI.F_TO_F_TO_F` | `E:f67/0405` | 3..8 | lo:FREG, value:FREG, hi:FREG | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FBNDXX` | `FBNDXX.F_TO_EA_TO_F` | `E:f67/0406` | 3..8 | lo:FREG, value:EA, hi:FREG | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FBNDXX` | `FBNDXX.F_TO_F_TO_F` | `E:f67/0407` | 3..8 | lo:FREG, value:FREG, hi:FREG | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FCOPYSIGN` | `FCOPYSIGN.F_TO_F_TO_F` | `E:f67/0408` | 3..8 | sign_src:FREG, magnitude_src:FREG, dst:FREG | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FMADD` | `FMADD.EA_TO_F_TO_F` | `E:f67/0409` | 3..8 | lhs:EA, rhs:FREG, dst:FREG | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FMADD` | `FMADD.F_TO_EA_TO_F` | `E:f67/040a` | 3..8 | lhs:FREG, rhs:EA, dst:FREG | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FMADD` | `FMADD.F_TO_F_TO_F` | `E:f67/040b` | 3..8 | lhs:FREG, rhs:FREG, dst:FREG | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FMSUB` | `FMSUB.EA_TO_F_TO_F` | `E:f67/040c` | 3..8 | lhs:EA, rhs:FREG, dst:FREG | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FMSUB` | `FMSUB.F_TO_EA_TO_F` | `E:f67/040d` | 3..8 | lhs:FREG, rhs:EA, dst:FREG | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FMSUB` | `FMSUB.F_TO_F_TO_F` | `E:f67/040e` | 3..8 | lhs:FREG, rhs:FREG, dst:FREG | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FNMADD` | `FNMADD.EA_TO_F_TO_F` | `E:f67/040f` | 3..8 | lhs:EA, rhs:FREG, dst:FREG | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FCLR` | `FCLR.F` | `E:f67/0410-041f` | 2..8 | dst:FREG | f:FREG[3:0] | instructions.yaml |
| `FNMADD` | `FNMADD.F_TO_EA_TO_F` | `E:f67/0420` | 3..8 | lhs:FREG, rhs:EA, dst:FREG | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FNMADD` | `FNMADD.F_TO_F_TO_F` | `E:f67/0421` | 3..8 | lhs:FREG, rhs:FREG, dst:FREG | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FNMSUB` | `FNMSUB.EA_TO_F_TO_F` | `E:f67/0422` | 3..8 | lhs:EA, rhs:FREG, dst:FREG | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FNMSUB` | `FNMSUB.F_TO_EA_TO_F` | `E:f67/0423` | 3..8 | lhs:FREG, rhs:EA, dst:FREG | e:EA/6@payload, f:FREG/4@payload, F:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FNMSUB` | `FNMSUB.F_TO_F_TO_F` | `E:f67/0424` | 3..8 | lhs:FREG, rhs:FREG, dst:FREG | f:FREG/4@payload, F:FREG/4@payload, f3:FREG/4@payload, z:S_D/1@payload | instructions.yaml |
| `FPOPM` | `FPOPM.BITMAP` | `E:f67/0425` | 3..8 | regs:fbitmap16 | b:fbitmap16/16@payload | instructions.yaml |
| `FPUSHM` | `FPUSHM.BITMAP` | `E:f67/0426` | 3..8 | regs:fbitmap16 | b:fbitmap16/16@payload | instructions.yaml |
| `FCLR` | `FCLR.EA` | `E:f67/0440-047f` | 2..8 | dst:EA | e:EA[5:0] | instructions.yaml |
| `FXCHG` | `FXCHG.F_TO_F` | `E:f67/0500-05ff` | 2..8 | lhs:FREG, rhs:FREG | f:FREG[3:0], F:FREG[7:4] | instructions.yaml |
| `FCEIL` | `FCEIL.F_TO_F` | `E:f67/0600-07ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FCEIL` | `FCEIL.EA_TO_F` | `E:f67/0800-0fff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FCEIL` | `FCEIL.F_TO_EA` | `E:f67/1000-17ff` | 2..8 | src:FREG, dst:EA | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FDIV` | `FDIV.EA_TO_F` | `E:f67/1800-1fff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FDIV` | `FDIV.F_TO_F` | `E:f67/2000-21ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FFLOOR` | `FFLOOR.F_TO_F` | `E:f67/2200-23ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FGETEXP` | `FGETEXP.F_TO_F` | `E:f67/2400-25ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FGETMAN` | `FGETMAN.F_TO_F` | `E:f67/2600-27ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FFLOOR` | `FFLOOR.EA_TO_F` | `E:f67/2800-2fff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FFLOOR` | `FFLOOR.F_TO_EA` | `E:f67/3000-37ff` | 2..8 | src:FREG, dst:EA | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FGETEXP` | `FGETEXP.EA_TO_F` | `E:f67/3800-3fff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FGETMAN` | `FGETMAN.EA_TO_F` | `E:f67/4000-47ff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FINT` | `FINT.EA_TO_F` | `E:f67/4800-4fff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FINT` | `FINT.F_TO_EA` | `E:f67/5000-57ff` | 2..8 | src:FREG, dst:EA | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FINT` | `FINT.F_TO_F` | `E:f67/5800-59ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FINTRZ` | `FINTRZ.F_TO_F` | `E:f67/5a00-5bff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FMAX` | `FMAX.F_TO_F` | `E:f67/5c00-5dff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FMIN` | `FMIN.F_TO_F` | `E:f67/5e00-5fff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FINTRZ` | `FINTRZ.EA_TO_F` | `E:f67/6000-67ff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FINTRZ` | `FINTRZ.F_TO_EA` | `E:f67/6800-6fff` | 2..8 | src:FREG, dst:EA | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FMAX` | `FMAX.EA_TO_F` | `E:f67/7000-77ff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FMIN` | `FMIN.EA_TO_F` | `E:f67/7800-7fff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FMOD` | `FMOD.EA_TO_F` | `E:f67/8000-87ff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FMOD` | `FMOD.F_TO_F` | `E:f67/8800-89ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FMUL` | `FMUL.F_TO_F` | `E:f67/8a00-8bff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FNEG` | `FNEG.F_TO_F` | `E:f67/8c00-8dff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FREM` | `FREM.F_TO_F` | `E:f67/8e00-8fff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FMUL` | `FMUL.EA_TO_F` | `E:f67/9000-97ff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FNEG` | `FNEG.EA_TO_F` | `E:f67/9800-9fff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FNEG` | `FNEG.F_TO_EA` | `E:f67/a000-a7ff` | 2..8 | src:FREG, dst:EA | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FREM` | `FREM.EA_TO_F` | `E:f67/a800-afff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FROUND` | `FROUND.EA_TO_F` | `E:f67/b000-b7ff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FROUND` | `FROUND.F_TO_EA` | `E:f67/b800-bfff` | 2..8 | src:FREG, dst:EA | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FROUND` | `FROUND.F_TO_F` | `E:f67/c000-c1ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FSCALE` | `FSCALE.F_TO_F` | `E:f67/c200-c3ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FSQRT` | `FSQRT.F_TO_F` | `E:f67/c400-c5ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FSUB` | `FSUB.F_TO_F` | `E:f67/c600-c7ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FSCALE` | `FSCALE.EA_TO_F` | `E:f67/c800-cfff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FSQRT` | `FSQRT.EA_TO_F` | `E:f67/d000-d7ff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FSQRT` | `FSQRT.F_TO_EA` | `E:f67/d800-dfff` | 2..8 | src:FREG, dst:EA | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FSUB` | `FSUB.EA_TO_F` | `E:f67/e000-e7ff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FTRUNC` | `FTRUNC.EA_TO_F` | `E:f67/e800-efff` | 2..8 | src:EA, dst:FREG | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FTRUNC` | `FTRUNC.F_TO_EA` | `E:f67/f000-f7ff` | 2..8 | src:FREG, dst:EA | e:EA[5:0], f:FREG[9:6], z:S_D[10] | instructions.yaml |
| `FTRUNC` | `FTRUNC.F_TO_F` | `E:f67/f800-f9ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FACOS` | `FACOS.F_TO_F` | `E:f68/0000-01ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FASIN` | `FASIN.F_TO_F` | `E:f68/0200-03ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FATAN` | `FATAN.F_TO_F` | `E:f68/0400-05ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FATANH` | `FATANH.F_TO_F` | `E:f68/0600-07ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FCOS` | `FCOS.F_TO_F` | `E:f68/0800-09ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FCOSH` | `FCOSH.F_TO_F` | `E:f68/0a00-0bff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FETOX` | `FETOX.F_TO_F` | `E:f68/0c00-0dff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FETOXM1` | `FETOXM1.F_TO_F` | `E:f68/0e00-0fff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FLOG10` | `FLOG10.F_TO_F` | `E:f68/1000-11ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FLOG2` | `FLOG2.F_TO_F` | `E:f68/1200-13ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FLOGN` | `FLOGN.F_TO_F` | `E:f68/1400-15ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FLOGNP1` | `FLOGNP1.F_TO_F` | `E:f68/1600-17ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FSIN` | `FSIN.F_TO_F` | `E:f68/1800-19ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FSINCOS` | `FSINCOS.F_TO_F` | `E:f68/1a00-1bff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FSINH` | `FSINH.F_TO_F` | `E:f68/1c00-1dff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FTAN` | `FTAN.F_TO_F` | `E:f68/1e00-1fff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FTANH` | `FTANH.F_TO_F` | `E:f68/2000-21ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FTENTOX` | `FTENTOX.F_TO_F` | `E:f68/2200-23ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `FTWOTOX` | `FTWOTOX.F_TO_F` | `E:f68/2400-25ff` | 2..8 | src:FREG, dst:FREG | f:FREG[3:0], F:FREG[7:4], z:S_D[8] | instructions.yaml |
| `ILLEGAL` | `ILLEGAL` | `P:fff` | 1..8 |  | none | instructions.yaml |
