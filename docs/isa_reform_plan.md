# ISA Reform Plan

Status: discussion summary, 2026-07-07.

This file captures the current ISA reform direction from the design discussion.
It is not yet the source of truth; the declarative YAML specs and generators
still need to be updated after the design settles.

## Base Instruction Header

The two-byte base instruction header uses the first byte's top two bits for instruction framing.

```text
byte 0 bit 7: Prefix Present (P)
byte 0 bit 6: Extended Format (X)
byte 0 bits 5-2 when X == 1: Additional Length in Bytes minus 1 (L)
```

Instruction length is determined directly from `P`, `X`, and `L`.

```text
if X == 0: instr_bytes = 2 + 2 * P
if X == 1: instr_bytes = 2 + 2 * P + (L + 1)
```

Equivalent size decoding truth table:

```text
15 14 13 12 11 10 | instr. bytes
0  0  x  x  x  x  | 2
1  0  x  x  x  x  | 4
0  1  0  0  0  0  | 3
0  1  0  0  0  1  | 4
0  1  0  0  1  0  | 5
0  1  0  0  1  1  | 6
0  1  0  1  0  0  | 7
0  1  0  1  0  1  | 8
0  1  0  1  1  0  | 9
0  1  0  1  1  1  | 10
0  1  1  0  0  0  | 11
0  1  1  0  0  1  | 12
0  1  1  0  1  0  | 13
0  1  1  0  1  1  | 14
0  1  1  1  0  0  | 15
0  1  1  1  0  1  | 16
0  1  1  1  1  0  | 17
0  1  1  1  1  1  | 18
1  1  0  0  0  0  | 5
1  1  0  0  0  1  | 6
1  1  0  0  1  0  | 7
1  1  0  0  1  1  | 8
1  1  0  1  0  0  | 9
1  1  0  1  0  1  | 10
1  1  0  1  1  0  | 11
1  1  0  1  1  1  | 12
1  1  1  0  0  0  | 13
1  1  1  0  0  1  | 14
1  1  1  0  1  0  | 15
1  1  1  0  1  1  | 16
1  1  1  1  0  0  | 17
1  1  1  1  0  1  | 18
1  1  1  1  1  0  | 19
1  1  1  1  1  1  | 20
```

This gives compact 2-byte instructions, compact-with-prefix 4-byte
instructions, extended 3-byte through 18-byte instructions, and
extended-with-prefix 5-byte through 20-byte instructions.

If `P` is set, a 16-bit prefix word immediately follows the base instruction
word and precedes any extended-format payload bytes. The prefix word contains two
8-bit prefix slots. The low byte is decoded first and the high byte is decoded
second. If `P` is clear, the instruction behaves as if both prefix slots were
`NPX`.

The first ten bits of the base word therefore determine instruction framing:
prefix presence, total instruction length, and the number of opcode/payload
bytes that follow. The remaining decode path is orthogonal:

```text
P=0, X=0       short instruction, 14-bit opcode payload
P=1, X=0       short instruction plus 16-bit prefix word
P=0/1, X=1     extended instruction, L+1 payload bytes
```

For `X=1, L=0`, the single payload byte combines with base-word payload bits to
form the 18-bit medium opcode payload. Medium opcodes whose high nibble is
`1111` are reserved as long/extralong escapes.

## General Registers

The new model keeps the current 16 general-purpose register capacity but removes
the architectural `An`/`Dn` split. General register fields are 4 bits.

```text
0000: R0
0001: R1
0010: R2
0011: R3
0100: R4
0101: R5
0110: R6
0111: R7
1000: R8
1001: R9
1010: R10
1011: R11
1100: R12
1101: R13
1110: R14
1111: R15
```

`SP` and `PC` remain special architectural registers outside the 4-bit `Rn`
namespace. `SP` normally uses `SS`; `PC` normally uses `CS`. This matches the
current ISA model where SP-relative forms have fixed `SS` and PC-relative forms
have fixed `CS`.

The core register file has no A/D split and no data-register bank selector.
The old DBANK mechanism is not part of the core architectural state; if extra
register files are needed later, they should be introduced as extension-owned
register classes rather than banked aliases of the core GPRs.

For 16-bit register bitmap operands, bit `i` selects `Rn(i)` for `i=0..15`.

## Segment Registers

The segment selector encoding remains unchanged.

```text
000: CS
001: DS
010: SS
011: GS0
100: GS1
101: GS2
110: GS3
111: GS4
```

Segment-qualified forms use an explicit segment field. SP- and PC-based special
forms omit the segment field and use their fixed architectural segments.

## Condition Codes

Condition code encodings are 4 bits.

```text
0000: T (true)
0001: F (false)
0010: EQ/Z  (Z == 1)
0011: NE/NZ (Z == 0)
0100: ULT/C (C == 1)
0101: UGE/NC (C == 0)
0110: MI/N  (N == 1)
0111: PL/NN (N == 0)
1000: VS/V  (V == 1)
1001: VC/NV (V == 0)
1010: ULE   (C == 1 || Z == 1)
1011: UGT   (C == 0 && Z == 0)
1100: LT    (N != V)
1101: GE    (N == V)
1110: LE    (Z == 1 || N != V)
1111: GT    (Z == 0 && N == V)
```

## Removed Core Instructions

The current core allocation does not carry these old core instructions:

```text
REVBIT
RCL
RCR
MADD
MSUB
GETDB
SELDB
MOVSETAD
MOVSETDA
MOVSETDD
XCHGSETAD
XCHGSETDA
XCHGSETDD
```

Carry rotates are not part of the scalar core. Multiword shift/rotate patterns
use the long `EXTRACT` funnel-extract form instead.

## Prefix Direction

Prefix slots are 8 bits. A full `REPcc Rn` form would consume all 8 bits
(`cc[3:0]` plus `Rn[3:0]`) and leave only the reclaimed `REPF` space for other
prefixes. To preserve prefix namespace, `REPcc` counters are restricted to
`R0-R7`.

Prefix namespace shape:

```text
0xxxxxxx  non-REP prefix namespace
1ccccrrr  REPcc R0-R7, except REPF is reserved
```

This preserves half of the 8-bit prefix space for non-repeat modifiers while
keeping the meaningful repeat condition set.

Concrete prefix slot allocation:

```text
00000000 NPX
00000001 NOSPEC
00000010 SATURATE
00000011 NONTEMPORAL
00000100 reserved
00000101 reserved
00000110 reserved
00000111 reserved
00001000 U2C
00001001 C2U
00001010 U2U
00001011..01111111 reserved

10000rrr REP/REPT Rr
10001rrr reserved        ; REPF reclaimed
10010rrr REPEQ/REPZ Rr
10011rrr REPNE/REPNZ Rr
10100rrr REPULT/REPC Rr
10101rrr REPUGE/REPNC Rr
10110rrr REPMI/REPN Rr
10111rrr REPPL/REPNN Rr
11000rrr REPVS/REPV Rr
11001rrr REPVC/REPNV Rr
11010rrr REPULE Rr
11011rrr REPUGT Rr
11100rrr REPLT Rr
11101rrr REPGE Rr
11110rrr REPLE Rr
11111rrr REPGT Rr
```

`rrr` names `R0-R7`. `REP Rr` is the canonical unconditional-repeat spelling
and aliases `REPT Rr`. `REPF Rr` is not assigned; its encoding range remains
reserved for future use.

The access-domain prefixes use the current meaning:

```text
U2C: source user-domain access, destination current-domain access
C2U: source current-domain access, destination user-domain access
U2U: source user-domain access, destination user-domain access
```

No prefix is needed for the default current-domain/current-domain case.

Prefix effects are applied in slot order. `NPX` has no effect. Prefixes in
different semantic groups combine when the instruction supports them. If two
prefixes in the same semantic group are present, the later slot wins. Reserved
prefix values are invalid instruction encodings.

The previous EA update prefixes (`POSTINC`, `PREINC`, `POSTDEC`, `PREDEC`) are
not kept as prefix concepts in the current direction. Auto-update is moving into
the EA encoding itself, using only postincrement and predecrement.

## Compact EA Encoding

EA fields are now 7 bits.

```text
000rrrr Rn(r)
001rrrr [Rn(r)]
010rrrr [Rn(r) + disp8s]
011rrrr [Rn(r) + disp16s]
100rrrr [Rn(r) + disp32s]
101rrrr [Rn(r) + disp64]
1100000 [SP + disp8s]
1100001 [SP + disp16s]
1100010 [SP + disp32s]
1100011 [SP + disp64]
1100100 [PC + disp8s]
1100101 [PC + disp16s]
1100110 [PC + disp32s]
1100111 [PC + disp64]
1101000 SP
1101001 [SP]
1101010 [abs32s]
1101011 [abs64]
1101100 imm8s
1101101 imm16s
1101110 imm32s
1101111 imm64
1110000 EXT0/disp8s
1110001 EXT0/disp16s
1110010 EXT0/disp32s
1110011 EXT0/disp64
1110100 EXT0 without displacement
1110101..1111111 reserved
```

Canonical encoding rule under consideration: unqualified `[Rn + disp]` should
use compact forms where available; EXT0 should be used for explicit segment,
indexed, zero-base, and auto-update forms.

## Immediate Encoding Rule

For medium, long, and extralong encodings, byte-sized or wider immediate
operands are carried only in one of two ways:

```text
1. an EA immediate form: imm8s, imm16s, imm32s, or imm64
2. a whole-byte payload field following the opcode or operand descriptor
```

They are not packed into partial opcode bitfields. This keeps immediate
canonicalization and future reclaim rules local: an immediate form can be
reclaimed by excluding one EA value or one payload descriptor, rather than by
recovering scattered opcode bits.

For payload-carrying medium forms, the first extended payload byte still
completes the 18-bit medium opcode. Any remaining bytes selected by `L` are
whole-byte operands. Example:

```text
00 0010 0111 1000 0000  ADD.Q <imm16s>, SP
00 0010 0111 1000 0001  ADD.Q <imm32s>, SP
00 0010 0111 1000 0010  SUB.Q <imm16s>, SP
00 0010 0111 1000 0011  SUB.Q <imm32s>, SP
```

The immediate bytes follow the 18-bit opcode as payload bytes; no immediate bits
are embedded in the opcode pattern.

Short encoding is the exception. It may pack explicitly listed 8-bit immediates
directly into the 14-bit short payload, such as `Jcc imm8s`, `JMP imm8s`, and
`ADD.Q imm8, SP` or `SUB.Q imm8, SP`.

`MOV.X imm, Rn` is represented by the medium `MOV.X <ea>, Rn` form with
`<ea> = imm8s/imm16s/imm32s/imm64`; it does not need a separate immediate
opcode family.

## Scale Rule

Indexed EA scale is implicit in the instruction rather than encoded in the EA
descriptor. The default rule should be:

```text
scale = memory operand element size in bytes
```

For ordinary memory operations this means byte = 1, word = 2, long = 4, and quad
= 8. `LEA.B/W/L/Q` uses the instruction suffix as the EA element size even
though it does not access memory. Other instructions without a normal memory
access size, such as `SEGLEA` and `PREFETCH`, still need an explicit
architectural rule. Open choices are a fixed quad scale or a size-bearing
instruction form.

Unscaled-index forms are not allocated. Byte-offset indexes such as
`load.q [base + byte_offset]` can be useful, but they create aliases when the
implicit scale is 1 and weaken the design rule that indexed addresses use
element indexes.

## EXT0 Encoding

Current EXT0 direction:

```text
0sssbbbb
  [SEG(s):Rn(b) + (displacement)]

1sss0000 bbbbiiii
  [SEG(s):Rn(b) + Rn(i)++ * scale + (displacement)]

1sss0001 bbbbiiii
  [SEG(s):Rn(b) + --Rn(i) * scale + (displacement)]

1sss0010 bbbbiiii
  [SEG(s):Rn(b) + Rn(i) * scale + (displacement)]

1sss0011
  [SEG(s):0 + (displacement)]

1sss1000 bbbb0000
  [SEG(s):Rn(b)++ + (displacement)]

1sss1000 bbbb0001
  [SEG(s):--Rn(b) + (displacement)]

1sss1001 0000iiii
  [SEG(s):0 + Rn(i)++ * scale + (displacement)]

1sss1001 0001iiii
  [SEG(s):0 + --Rn(i) * scale + (displacement)]

1sss1001 0010iiii
  [SEG(s):0 + Rn(i) * scale + (displacement)]

10001010 0000iiii
  [SP + Rn(i)++ * scale + (displacement)]

10001010 0001iiii
  [SP + --Rn(i) * scale + (displacement)]

10001010 0010iiii
  [SP + Rn(i) * scale + (displacement)]

10001011 0000iiii
  [PC + Rn(i)++ * scale + (displacement)]

10001011 0001iiii
  [PC + --Rn(i) * scale + (displacement)]

10001011 0010iiii
  [PC + Rn(i) * scale + (displacement)]

1bbbb100
  [Rn(b)++ + (displacement)]

1bbbb101
  [--Rn(b) + (displacement)]
```

The `10001010` and `10001011` forms are exact SP/PC opcodes, not segment-coded
forms. SP uses `SS`; PC uses `CS`.

The short `1bbbb100` and `1bbbb101` forms are default-segment aliases for common
base auto-update access. They overlap semantically with explicit `SEG` forms, so
the assembler should prefer the short form when no segment is written.

Reserved holes should stay explicitly reserved for now, especially around
`1sss0100..1sss0111`, unused `1sss1000` low-bit combinations, unused
`1sss1001` submodes, and unused SP/PC exact submodes.

## Auto-Update Semantics

Only postincrement and predecrement are carried forward.

```text
Rn++  uses the old value for the term, then updates the temporary value upward
--Rn  updates the temporary value downward first, then uses the new value
```

For base auto-update, the delta is the memory access size in bytes. For index
auto-update, the delta is one element before scaling. Example:

```text
[Rb + Ri++ * scale]
  uses old Ri in the address term
  then Ri_temp = old Ri + 1

[Rb + --Ri * scale]
  first Ri_temp = old Ri - 1
  then uses Ri_temp in the address term
```

The preferred architectural model is sequential operand evaluation with a
temporary register image and commit-time architectural updates.

```text
1. Snapshot architectural registers into a temporary operand-evaluation image.
2. Evaluate operands in the defined instruction operand order.
3. Auto-update addressing modes update only the temporary image.
4. Memory reads and writes are collected as instruction side effects.
5. No architectural register or memory side effect becomes visible before commit.
6. If the instruction faults before commit, architectural state is unchanged
   except for architecturally defined exception entry state.
```

This preserves m68k-like sequential meaning without requiring m68k-style
mid-instruction architectural updates.

Example:

```text
MOV.B [R1++], [R1++]
initial R1 = x

source EA = x
temporary R1 = x + 1
destination EA = x + 1
temporary R1 = x + 2

commit:
  mem[x + 1] = mem[x]
  R1 = x + 2
```

Same-register use inside one EA is allowed under this model because the
sequential temporary-image rule makes it unambiguous.

Examples:

```text
[R1 + R1++ * scale]
  base term uses current temporary R1
  index term uses current temporary R1, then increments temporary R1 by 1

[R1 + --R1 * scale]
  base term uses current temporary R1
  index term decrements temporary R1 by 1, then uses the updated temporary R1
```

Open detail: the intra-EA term evaluation order should be specified. A practical
choice is base term first, then index term, then displacement.

REP interaction: each REP iteration should commit independently. A fault after
some iterations preserves already committed iterations and restarts from the last
committed architectural state.

## Short Encoding

Short encodings are 14 payload bits after `P=0, X=0`.

Concrete short payload allocation:

```text
00 000z ssss dddd  MOV.X(z:L/Q) Rn(s), Rn(d)
00 001z ssss dddd  ADD.X(z:L/Q) Rn(s), Rn(d)
00 010z ssss dddd  SUB.X(z:L/Q) Rn(s), Rn(d)
00 011z ssss dddd  CMP.X(z:L/Q) Rn(s), Rn(d)
00 100z ssss dddd  AND.X(z:L/Q) Rn(s), Rn(d)
00 101z ssss dddd  OR.X(z:L/Q)  Rn(s), Rn(d)
00 110z ssss dddd  XOR.X(z:L/Q) Rn(s), Rn(d)
00 111z ssss dddd  TEST.X(z:L/Q) Rn(s), Rn(d)

01 000z ssss dddd  XCHG.X(z:L/Q) Rn(s), Rn(d)
01 001z ssss dddd  SHR.X(z:L/Q) Rn(s), Rn(d)
01 010z ssss dddd  SHL.X(z:L/Q) Rn(s), Rn(d)
01 011z ssss dddd  ROR.X(z:L/Q) Rn(s), Rn(d)
01 100z ssss dddd  ROL.X(z:L/Q) Rn(s), Rn(d)
01 101z ssss dddd  SAR.X(z:L/Q) Rn(s), Rn(d)
01 110z ssss dddd  EXTZL.X(z:B/W) Rn(s), Rn(d)
01 111z ssss dddd  EXTSL.X(z:B/W) Rn(s), Rn(d)

10 0000 0000 ssss  MOV.Q Rn(s), SP
10 0000 0001 dddd  MOV.Q SP, Rn(d)
10 0000 0010 rrrr  PUSH Rn(r)
10 0000 0011 rrrr  POP Rn(r)
10 0000 0100 0000  NOP
10 0000 0100 0001  RET
10 0000 0100 0010  LRET
10 0000 0100 0011  SYSCALL
10 0000 0100 0100  SYSRET
10 0000 0100 0101  IRET
10 0000 0100 0110  BKPT
10 0000 0100 0111  WAIT
10 0000 0100 1000  YIELD
10 0000 0100 1001  HALT
10 0000 0100 1010  ILLEGAL
10 0000 0100 1011  RFENCE
10 0000 0100 1100  WFENCE
10 0000 0100 1101  AFENCE
10 0000 0100 1110  RESET
10 0000 0101 0000  TRAP
10 0000 0101 0001  reserved
10 0000 0101 cccc  TRAPcc  ; cccc = 0010..1111
10 0001 rrrr 0000  SET Rn(r)
10 0001 rrrr 0001  reserved
10 0001 rrrr cccc  SETcc Rn(r)  ; cccc = 0010..1111
10 001z 0000 rrrr  INC.X(z:L/Q) Rn(r)
10 001z 0001 rrrr  DEC.X(z:L/Q) Rn(r)
10 001z 0010 rrrr  NEG.X(z:L/Q) Rn(r)
10 001z 0011 rrrr  CLR.X(z:L/Q) Rn(r)
10 001z 0100 rrrr  ABS.X(z:L/Q) Rn(r)
10 001z 0101 rrrr  NOT.X(z:L/Q) Rn(r)
10 0010 1001 rrrr  REVBYTE.W Rn(r)
10 0010 1010 rrrr  REVBYTE.L Rn(r)
10 0010 1011 rrrr  REVBYTE.Q Rn(r)
10 1000 ssss dddd  EXTZQ.L Rn(s), Rn(d)
10 1001 ssss dddd  EXTSQ.L Rn(s), Rn(d)
10 1111 iiii iiii  ADD.Q imm8(i), SP

11 0000 iiii iiii  JMP imm8s(i)
11 0001 0000 0000  reserved
11 0001 iiii iiii  SUB.Q imm8(i), SP  ; i = 00000001..11111111
11 cccc iiii iiii  Jcc imm8s(i)  ; cccc = 0010..1111
```

Any short payload value not matched by this table is reserved.

Concrete allocation summary:

```text
assigned instructions        13,629
reserved encodings           2,755
total short payload values   16,384
```

## Medium Encoding Direction

Medium encodings are 18 payload bits. They are the main home for one-register
plus compact-EA forms, register/EA arithmetic, register/EA shifts, EA unary
forms, and long/extralong escapes.

The long/extralong escape block is selected by the high nibble of the medium
opcode payload:

```text
medium_payload[17:14] != 1111  medium opcode
medium_payload[17:14] == 1111  long/extralong escape namespace
```

At the wider opcode-payload level, the escape namespace is split between ordinary
long encodings and extralong encodings.

### Concrete Medium Payload Allocation

The concrete medium payload map uses 18-bit payload values. Any medium payload
value not matched by this table is reserved.

```text
00 00?0 ???? ?110 1000  reserved
0? ???1 ???? ?110 1000  reserved

00 ??10 0110 0000 0001  reserved

00 0010 0110 0000 0000  JMP <imm16s>
00 0010 0110 0000 cccc  Jcc <imm16s>  ; cccc = 0010..1111
00 0110 0110 0000 0000  JMP <imm32s>
00 0110 0110 0000 cccc  Jcc <imm32s>  ; cccc = 0010..1111
00 1010 0110 0000 0000  CALL <imm16s>
00 1010 0110 0000 cccc  CALLcc <imm16s>  ; cccc = 0010..1111
00 1110 0110 0000 0000  CALL <imm32s>
00 1110 0110 0000 cccc  CALLcc <imm32s>  ; cccc = 0010..1111

01 zz10 0110 0000 dddd  SUM.X(z:B/W/L/Q) <imm16/bitmap>, Rn(d)

00 0010 0110 1000 rrrr  REPG Rn(r), <imm16>
00 0010 0111 0000 rrrr  CPUID Rn(r)

00 0010 0111 1000 0000  ADD.Q <imm16s>, SP
00 0010 0111 1000 0001  ADD.Q <imm32s>, SP
00 0010 0111 1000 0010  SUB.Q <imm16s>, SP
00 0010 0111 1000 0011  SUB.Q <imm32s>, SP
00 0010 0111 1000 0100  PUSHM <imm16/bitmap>
00 0010 0111 1000 0101  POPM <imm16/bitmap>
00 0010 0111 1000 0110  TRACE <imm16>
00 0010 0111 1000 0111  reserved
00 0010 0111 1000 1???  reserved

0e ee10 z000 0000 eeee  INC.X(z:B/W) <ea>
0e ee10 z000 1000 eeee  INC.X(z:L/Q) <ea>  ; <ea>[6:4] = 001..111
0e ee10 z001 0000 eeee  DEC.X(z:B/W) <ea>
0e ee10 z001 1000 eeee  DEC.X(z:L/Q) <ea>  ; <ea>[6:4] = 001..111
0e ee10 z010 0000 eeee  NEG.X(z:B/W) <ea>
0e ee10 z010 1000 eeee  NEG.X(z:L/Q) <ea>  ; <ea>[6:4] = 001..111
0e ee10 z011 0000 eeee  CLR.X(z:B/W) <ea>
0e ee10 z011 1000 eeee  CLR.X(z:L/Q) <ea>  ; <ea>[6:4] = 001..111
0e ee10 z100 0000 eeee  ABS.X(z:B/W) <ea>
0e ee10 z100 1000 eeee  ABS.X(z:L/Q) <ea>  ; <ea>[6:4] = 001..111
0e ee10 z101 0000 eeee  NOT.X(z:B/W) <ea>
0e ee10 z101 1000 eeee  NOT.X(z:L/Q) <ea>  ; <ea>[6:4] = 001..111

0e ee10 0110 1000 eeee  REVBYTE.W <ea>  ; <ea>[6:4] = 001..111
0e ee10 0111 0000 eeee  REVBYTE.L <ea>  ; <ea>[6:4] = 001..111
0e ee10 0111 1000 eeee  REVBYTE.Q <ea>  ; <ea>[6:4] = 001..111

0e eez1 zddd d000 eeee  LEA.X(z:B/W/L/Q) <ea>, Rn

00 0000 zsss seee eeee  MOV.X(z:B/W) Rn(s), <ea>(e)  ; <ea> = 0000000..1100111 + 1101001..1111111
00 0001 zsss seee eeee  MOV.X(z:L/Q) Rn(s), <ea>(e)  ; <ea> = 0010000..1100111 + 1101001..1111111
00 0010 zddd deee eeee  MOV.X(z:B/W) <ea>(e), Rn(d)  ; <ea> = 0010000..1100111 + 1101001..1111111
00 0011 zddd deee eeee  MOV.X(z:L/Q) <ea>(e), Rn(d)  ; <ea> = 0010000..1100111 + 1101001..1111111

00 0100 zsss seee eeee  ADD.X(z:B/W) Rn(s), <ea>(e)
00 0101 zsss seee eeee  ADD.X(z:L/Q) Rn(s), <ea>(e)  ; <ea> = 0010000..1100111 + 1101001..1111111
00 0110 zddd deee eeee  ADD.X(z:B/W) <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
00 0111 zddd deee eeee  ADD.X(z:L/Q) <ea>(e), Rn(d)  ; <ea> = 0010000..1100111 + 1101001..1111111
00 1000 zsss seee eeee  SUB.X(z:B/W) Rn(s), <ea>(e)
00 1001 zsss seee eeee  SUB.X(z:L/Q) Rn(s), <ea>(e)  ; <ea> = 0010000..1100111 + 1101001..1111111
00 1010 zddd deee eeee  SUB.X(z:B/W) <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
00 1011 zddd deee eeee  SUB.X(z:L/Q) <ea>(e), Rn(d)  ; <ea> = 0010000..1100111 + 1101001..1111111
00 1100 zsss seee eeee  AND.X(z:B/W) Rn(s), <ea>(e)
00 1101 zsss seee eeee  AND.X(z:L/Q) Rn(s), <ea>(e)  ; <ea> = 0010000..1100111 + 1101001..1111111
00 1110 zddd deee eeee  AND.X(z:B/W) <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
00 1111 zddd deee eeee  AND.X(z:L/Q) <ea>(e), Rn(d)  ; <ea> = 0010000..1100111 + 1101001..1111111

01 0000 zsss seee eeee  OR.X(z:B/W) Rn(s), <ea>(e)
01 0001 zsss seee eeee  OR.X(z:L/Q) Rn(s), <ea>(e)  ; <ea> = 0010000..1100111 + 1101001..1111111
01 0010 zddd deee eeee  OR.X(z:B/W) <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
01 0011 zddd deee eeee  OR.X(z:L/Q) <ea>(e), Rn(d)  ; <ea> = 0010000..1100111 + 1101001..1111111
01 0100 zsss seee eeee  XOR.X(z:B/W) Rn(s), <ea>(e)
01 0101 zsss seee eeee  XOR.X(z:L/Q) Rn(s), <ea>(e)  ; <ea> = 0010000..1100111 + 1101001..1111111
01 0110 zddd deee eeee  XOR.X(z:B/W) <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
01 0111 zddd deee eeee  XOR.X(z:L/Q) <ea>(e), Rn(d)  ; <ea> = 0010000..1100111 + 1101001..1111111
01 1000 zsss seee eeee  TEST.X(z:B/W) Rn(s), <ea>(e)
01 1001 zsss seee eeee  TEST.X(z:L/Q) Rn(s), <ea>(e)  ; <ea> = 0010000..1100111 + 1101001..1111111
01 1010 zddd deee eeee  TEST.X(z:B/W) <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
01 1011 zddd deee eeee  TEST.X(z:L/Q) <ea>(e), Rn(d)  ; <ea> = 0010000..1100111 + 1101001..1111111
01 1100 zsss seee eeee  CMP.X(z:B/W) Rn(s), <ea>(e)
01 1101 zsss seee eeee  CMP.X(z:L/Q) Rn(s), <ea>(e)  ; <ea> = 0010000..1100111 + 1101001..1111111
01 1110 zddd deee eeee  CMP.X(z:B/W) <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
01 1111 zddd deee eeee  CMP.X(z:L/Q) <ea>(e), Rn(d)  ; <ea> = 0010000..1100111 + 1101001..1111111

10 0000 zsss seee eeee  XCHG.X(z:B/W) Rn(s), <ea>(e)
10 0001 zsss seee eeee  XCHG.X(z:L/Q) Rn(s), <ea>(e)  ; <ea> = 0010000..1100111 + 1101001..1111111
10 0010 zddd deee eeee  XCHG.X(z:B/W) <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
10 0011 zddd deee eeee  XCHG.X(z:L/Q) <ea>(e), Rn(d)  ; <ea> = 0010000..1100111 + 1101001..1111111

10 0111 ???? ?000 ????  reserved
10 1??1 ???? ?000 ????  reserved

10 0110 zsss seee eeee  ROL.X(z:B/W) Rn(s), <ea>(e)
10 0111 zsss seee eeee  ROL.X(z:L/Q) Rn(s), <ea>(e)  ; <ea>[6:4] = 001..111
10 1000 zsss seee eeee  ROR.X(z:B/W) Rn(s), <ea>(e)
10 1001 zsss seee eeee  ROR.X(z:L/Q) Rn(s), <ea>(e)  ; <ea>[6:4] = 001..111
10 1010 zsss seee eeee  SHL.X(z:B/W) Rn(s), <ea>(e)
10 1011 zsss seee eeee  SHL.X(z:L/Q) Rn(s), <ea>(e)  ; <ea>[6:4] = 001..111
10 1100 zsss seee eeee  SHR.X(z:B/W) Rn(s), <ea>(e)
10 1101 zsss seee eeee  SHR.X(z:L/Q) Rn(s), <ea>(e)  ; <ea>[6:4] = 001..111
10 1110 zsss seee eeee  SAR.X(z:B/W) Rn(s), <ea>(e)
10 1111 zsss seee eeee  SAR.X(z:L/Q) Rn(s), <ea>(e)  ; <ea>[6:4] = 001..111

11 00zz 1sss s000 dddd  ADC.X(z:B/W/L/Q) Rn(s), Rn(d)

11 0?11 0??? ?000 ????  reserved
11 10?? 1??? ?000 ????  reserved

11 0000 0sss seee eeee  EXTSW.B Rn(s), <ea>(e)
11 0000 1ddd deee eeee  EXTSW.B <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
11 0001 0sss seee eeee  EXTSQ.B Rn(s), <ea>(e)
11 0001 1ddd deee eeee  EXTSQ.B <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
11 0010 0sss seee eeee  EXTSQ.W Rn(s), <ea>(e)
11 0010 1ddd deee eeee  EXTSQ.W <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
11 0011 0sss seee eeee  EXTSQ.L Rn(s), <ea>(e)  ; <ea>[6:4] = 001..111
11 0011 1ddd deee eeee  EXTSQ.L <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111

11 01zz 1sss s000 dddd  SBB.X(z:B/W/L/Q) Rn(s), Rn(d)

11 0100 0sss seee eeee  EXTZW.B Rn(s), <ea>(e)
11 0100 1ddd deee eeee  EXTZW.B <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
11 0101 0sss seee eeee  EXTZQ.B Rn(s), <ea>(e)
11 0101 1ddd deee eeee  EXTZQ.B <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
11 0110 0sss seee eeee  EXTZQ.W Rn(s), <ea>(e)
11 0110 1ddd deee eeee  EXTZQ.W <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
11 0111 0sss seee eeee  EXTZQ.L Rn(s), <ea>(e)  ; <ea>[6:4] = 001..111
11 0111 1ddd deee eeee  EXTZQ.L <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111

11 1000 0sss seee eeee  EXTSL.B Rn(s), <ea>(e)  ; <ea>[6:4] = 001..111
11 1000 1ddd deee eeee  EXTSL.B <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
11 1001 0sss seee eeee  EXTSL.W Rn(s), <ea>(e)  ; <ea>[6:4] = 001..111
11 1001 1ddd deee eeee  EXTSL.W <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111

11 1010 0sss seee eeee  EXTZL.B Rn(s), <ea>(e)  ; <ea>[6:4] = 001..111
11 1010 1ddd deee eeee  EXTZL.B <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111
11 1011 0sss seee eeee  EXTZL.W Rn(s), <ea>(e)  ; <ea>[6:4] = 001..111
11 1011 1ddd deee eeee  EXTZL.W <ea>(e), Rn(d)  ; <ea>[6:4] = 001..111

11 11?? ???? ???? ????  long/extralong escape
```

Concrete medium allocation summary:

```text
assigned instructions        229,555
long/extralong escapes         16,384
reserved encodings            16,205
total medium payload values  262,144
```

## Long Encoding Direction

Long and extralong encodings are reached through the 16K medium escape namespace.
The opcode-payload split is:

```text
11 110? ???? ???? ???? ???? ????       long encoding
11 1110 ???? ???? ???? ???? ????       long encoding
11 1111 ???? ???? ???? ???? ???? ???? ????  extralong encoding
```

The shown bit strings are opcode payload bits after the first ten framing bits.
Additional payload bytes carry opcode extension bits, descriptors, EA payloads,
or immediates as selected by the instruction format.

Long encodings are intended for wider operand descriptions:

```text
two-EA forms
EA + immediate forms
EA + two-register forms
funnel extraction and bit operations
multiply and divide forms
atomics
system/cache/TLB forms with selectors
```

### Concrete Long Payload Allocation

Long payload patterns below are 26 opcode-payload bits. Payload values not
matched by the table are reserved.

Reclaim notation:

```text
reclaim e.rn       reserve encodings where EA field e is Rn direct
reclaim e.reg      reserve encodings where EA field e is Rn direct or SP direct
reclaim s.reg      same rule for a source EA field
reclaim d.reg      same rule for a destination EA field
dst !imm           destination EA immediate forms are invalid/reserved
```

Values excluded by a reclaim or invalid-destination note are reserved. For
two-EA forms, direct-register operands are reclaimed even when the direct
register is `SP`; this keeps the canonical path through short/medium or
register-specific long forms.

Concrete long allocation:

```text
11 1100 0000 zz00 0sss seee eeee  ADC.X(z:B/W/L/Q) Rn(s), <ea>(e)  ; reclaim e.rn, dst !imm
11 1100 0000 zz00 1sss seee eeee  ADC.X(z:B/W/L/Q) <ea>(e), Rn(s)  ; reclaim e.rn
11 1100 0000 zz01 0sss seee eeee  SBB.X(z:B/W/L/Q) Rn(s), <ea>(e)  ; reclaim e.rn, dst !imm
11 1100 0000 zz01 1sss seee eeee  SBB.X(z:B/W/L/Q) <ea>(e), Rn(s)  ; reclaim e.rn

11 1100 0000 zz10 0ddd deee eeee  CLZ.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0000 zz10 1ddd deee eeee  CTZ.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0000 zz11 0ddd deee eeee  CLS.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0000 zz11 1ddd deee eeee  CTS.X(z:B/W/L/Q) <ea>(e), Rn(d)

11 1100 0001 zz00 0ddd deee eeee  MINU.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0001 zz00 1sss seee eeee  MINU.X(z:B/W/L/Q) Rn(s), <ea>(e)  ; reclaim e.rn, dst !imm
11 1100 0001 zz01 0ddd deee eeee  MINS.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0001 zz01 1sss seee eeee  MINS.X(z:B/W/L/Q) Rn(s), <ea>(e)  ; reclaim e.rn, dst !imm
11 1100 0001 zz10 0ddd deee eeee  MAXU.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0001 zz10 1sss seee eeee  MAXU.X(z:B/W/L/Q) Rn(s), <ea>(e)  ; reclaim e.rn, dst !imm
11 1100 0001 zz11 0ddd deee eeee  MAXS.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0001 zz11 1sss seee eeee  MAXS.X(z:B/W/L/Q) Rn(s), <ea>(e)  ; reclaim e.rn, dst !imm

11 1100 0010 zz00 0ddd deee eeee  POPCNT.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0010 zz00 1ddd deee eeee  PARITY.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0010 zz01 0ddd deee eeee  MUL.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0010 zz01 1ddd deee eeee  CLMUL.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0010 zz10 0ddd deee eeee  DIVU.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0010 zz10 1ddd deee eeee  DIVS.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0010 zz11 0ddd deee eeee  MODU.X(z:B/W/L/Q) <ea>(e), Rn(d)
11 1100 0010 zz11 1ddd deee eeee  MODS.X(z:B/W/L/Q) <ea>(e), Rn(d)

11 1100 0011 0000 0bbb beee eeee  BTEST Rn(b), <ea>(e)
11 1100 0011 0000 1bbb beee eeee  BSET Rn(b), <ea>(e)  ; dst !imm
11 1100 0011 0001 0bbb beee eeee  BCLR Rn(b), <ea>(e)  ; dst !imm
11 1100 0011 0001 1bbb beee eeee  BCHG Rn(b), <ea>(e)  ; dst !imm
11 1100 0011 0010 0ccc ceee eeee  DJcc Rn(c), <ea>(e)
11 1100 0011 0010 1rrr reee eeee  LCALL Rn(r), <ea>(e)
11 1100 0011 0011 0rrr reee eeee  LJMP Rn(r), <ea>(e)
11 1100 0011 0011 1ddd deee eeee  CLMULH.Q <ea>(e), Rn(d)

11 1100 0100 zz11 0000 0eee eeee  SEGLEA.X(z:B/W/L/Q) <ea>(e)
11 1100 0100 zz11 0000 1000 rrrr  INCN.X(z:B/W/L/Q) Rn(r)
11 1100 0100 zz11 0000 1001 rrrr  DECN.X(z:B/W/L/Q) Rn(r)

11 1110 0000 zzss ssss sddd dddd  MOV.X(z:B/W/L/Q) <ea>(s), <ea>(d)  ; reclaim s.reg | d.reg, dst !imm
11 1110 0001 zzss ssss sddd dddd  CMP.X(z:B/W/L/Q) <ea>(s), <ea>(d)  ; reclaim s.reg | d.reg

11 1110 1000 00ss ssss sddd dddd  EXTSW.B <ea>(s), <ea>(d)  ; reclaim s.reg | d.reg, dst !imm
11 1110 1000 01ss ssss sddd dddd  EXTSQ.B <ea>(s), <ea>(d)  ; reclaim s.reg | d.reg, dst !imm
11 1110 1000 10ss ssss sddd dddd  EXTSQ.W <ea>(s), <ea>(d)  ; reclaim s.reg | d.reg, dst !imm
11 1110 1000 11ss ssss sddd dddd  EXTSQ.L <ea>(s), <ea>(d)  ; reclaim s.reg | d.reg, dst !imm

11 1110 1001 00ss ssss sddd dddd  EXTZW.B <ea>(s), <ea>(d)  ; reclaim s.reg | d.reg, dst !imm
11 1110 1001 01ss ssss sddd dddd  EXTZQ.B <ea>(s), <ea>(d)  ; reclaim s.reg | d.reg, dst !imm
11 1110 1001 10ss ssss sddd dddd  EXTZQ.W <ea>(s), <ea>(d)  ; reclaim s.reg | d.reg, dst !imm
11 1110 1001 11ss ssss sddd dddd  EXTZQ.L <ea>(s), <ea>(d)  ; reclaim s.reg | d.reg, dst !imm

11 1110 1010 0zss ssss sddd dddd  EXTSL.X(z:B/W) <ea>(s), <ea>(d)  ; reclaim s.reg | d.reg, dst !imm
11 1110 1010 1zss ssss sddd dddd  EXTZL.X(z:B/W) <ea>(s), <ea>(d)  ; reclaim s.reg | d.reg, dst !imm

11 1110 1100 zz0i iiii ieee eeee  ROL.X(z:B/W/L/Q) imm6(i), <ea>(e)  ; dst !imm
11 1110 1100 zz1i iiii ieee eeee  ROR.X(z:B/W/L/Q) imm6(i), <ea>(e)  ; dst !imm
11 1110 1101 zz0i iiii ieee eeee  SHL.X(z:B/W/L/Q) imm6(i), <ea>(e)  ; dst !imm
11 1110 1101 zz1i iiii ieee eeee  SHR.X(z:B/W/L/Q) imm6(i), <ea>(e)  ; dst !imm
11 1110 1110 zz0i iiii ieee eeee  SAR.X(z:B/W/L/Q) imm6(i), <ea>(e)  ; dst !imm

11 1110 1110 001i iiii ieee eeee  BTEST imm6(i), <ea>(e)
11 1110 1110 011i iiii ieee eeee  BSET imm6(i), <ea>(e)  ; dst !imm
11 1110 1110 101i iiii ieee eeee  BCLR imm6(i), <ea>(e)  ; dst !imm
11 1110 1110 111i iiii ieee eeee  BCHG imm6(i), <ea>(e)  ; dst !imm

11 1110 1111 00ii iddd deee eeee  PTQUERY imm3(i), <ea>(e), Rn(d)
11 1110 1111 0100 0000 vvvv pppp  VTOP Rn(v), Rn(p)
11 1110 1111 0100 0001 pppp aaaa  SWPTA Rn(p), Rn(a)
11 1110 1111 0100 0010 0sss dddd  RDSEG SREG(s), Rn(d)
11 1110 1111 0100 0010 1sss dddd  WRSEG Rn(d), SREG(s)
11 1110 1111 0100 0011 0eee eeee  INVPAGE <ea>(e)
11 1110 1111 0100 0011 1eee eeee  FLSHDCACHE <ea>(e)
11 1110 1111 0100 0100 0eee eeee  INVDCACHE <ea>(e)
11 1110 1111 0100 0100 1eee eeee  INVICACHE <ea>(e)
11 1110 1111 0100 0101 0eee eeee  PREFETCH <ea>(e)
11 1110 1111 0100 0101 1eee eeee  SYNCCACHE <ea>(e)
11 1110 1111 0100 0110 0eee eeee  WRBKDCACHE <ea>(e)
11 1110 1111 0100 0110 1eee eeee  SAVE <ea>(e)
11 1110 1111 0100 0111 0eee eeee  RESTORE <ea>(e)

11 1110 1111 0100 1000 0000 dddd  RDCR <imm16>, Rn(d)
11 1110 1111 0100 1000 0001 ssss  WRCR Rn(s), <imm16>
11 1110 1111 0100 1000 0010 dddd  RDFLAGS Rn(d)
11 1110 1111 0100 1000 0011 ssss  WRFLAGS Rn(s)
11 1110 1111 0100 1000 0100 dddd  RDFFLAGS Rn(d)
11 1110 1111 0100 1000 0101 ssss  WRFFLAGS Rn(s)
11 1110 1111 0100 1000 0110 dddd  RDSTATUS Rn(d)
11 1110 1111 0100 1000 0111 ssss  WRSTATUS Rn(s)
11 1110 1111 0100 1000 1000 dddd  RDFSTATUS Rn(d)
11 1110 1111 0100 1000 1001 ssss  WRFSTATUS Rn(s)
11 1110 1111 0100 1000 1010 dddd  RDPMC <imm16>, Rn(d)
11 1110 1111 0100 1000 1011 pppp  SWPT Rn(p)

11 1110 1111 0100 1111 0000 0000  INVASID <imm16>
11 1110 1111 0100 1111 0000 0001  INVTLB

11 1110 1111 1000 0000 ssss dddd  MULHU.Q Rn(s), Rn(d)
11 1110 1111 1000 0001 ssss dddd  MULHS.Q Rn(s), Rn(d)
11 1110 1111 1000 0010 ssss dddd  MULHSU.Q Rn(s), Rn(d)
```

Concrete long allocation summary after reclaim:

```text
ordinary long payload values     3,145,728
raw matched payload values         757,186
reclaimed/invalid payload values   104,172
assigned payload values            653,014
reserved payload values          2,492,714
overlaps                                 0
```

Funnel-extract direction:

```text
EXTRACT.X(z:B/W/L/Q) imm7(i), Rn(high), Rn(low/dest)
  N = operand size in bits
  Rn(low/dest) = low_N(concat_N(Rn(high), Rn(low/dest)) >> i)
```

For each size, only `i = 0..(2*N - 1)` is valid. Larger `imm7` values for
smaller operand sizes are reserved. `EXTRACT` does not consume or produce carry
flags; carry-through rotates remain unallocated.

Integer multiply direction:

```text
MUL.B/W/L/Q <ea>, Rn
  Rn = low_N(Rn * value(<ea>))
  signed and unsigned low-half multiply share this form

MULHU.Q Rn(s), Rn(d)
  Rn(d) = high_64(unsigned(Rn(d)) * unsigned(Rn(s)))

MULHS.Q Rn(s), Rn(d)
  Rn(d) = high_64(signed(Rn(d)) * signed(Rn(s)))

MULHSU.Q Rn(s), Rn(d)
  Rn(d) = high_64(signed(Rn(d)) * unsigned(Rn(s)))
```

There are no separate low-half `MULU` and `MULS` forms. Sub-quad high-half
multiply forms are not allocated; narrower operands should be extended to quad
before using the Q-only `MULH*` forms.

Integer multiply-accumulate forms (`MADD`, `MSUB`) are not allocated in the
core integer ISA. Dot-product and widening MAC-style operations belong in a
future DSP/vector-oriented extension rather than the scalar core encoding.

The ordinary long space uses the three non-`111111` quarters of the escape
namespace. The `111111` quarter is reserved for extralong encodings that need
another opcode-payload byte before descriptors or operand payloads.

## Encoding Allocation Strategy

The previous allocation flow used Z3 to pack instruction encodings from a broad
instruction set and coarse usage weights. The current reform direction should move
the primary source of truth to hand-authored allocation tables.

The reason is that the important choices are structural rather than numeric:

```text
short encodings: manually chosen hot register/control forms
medium encodings: manually chosen one-register, small-displacement, and one-EA forms
long encodings: manually chosen wide operand forms, atomics, system forms
EA encodings: manually designed canonical and extended forms
prefix encodings: manually reserved namespace with REPcc constrained to R0-R7
```

The existing weight model is not granular enough to justify solver-driven
placement. A solver can optimize the wrong objective when the real tradeoffs are
canonical form selection, namespace shape, alias avoidance, decoder regularity,
and future extension room.

Recommended flow:

```text
hand-authored allocation tables
  -> collision and consistency validator
  -> generated decoder, assembler, disassembler, and RTL tables
  -> encode/decode/disassemble roundtrip tests
```

The validator should check at least:

```text
bit-pattern overlap
length class and payload byte consistency
declared mask/pattern cardinality versus actual covered encodings
required contiguous or masked subspace availability for each form family
reserved range violations
duplicate canonical encodings for the same form
EA and EXT0 descriptor collisions
prefix namespace collisions
assembler encode -> disassemble -> encode stability
```

`alloc_z3.py` can remain as an exploratory helper for finding empty space or
testing trial packings, but it should no longer be the primary allocation
authority.

## Main Open Items

1. Define scale for `SEGLEA`, `PREFETCH`, and any no-memory-access EA
   calculation instruction that does not carry an explicit size suffix.
2. Specify intra-EA term evaluation order for auto-update cases.
3. Define precise commit/fault behavior for multi-memory instructions.
4. Decide whether index auto-update is worth keeping or whether only base
   auto-update should remain.
5. Replace the primary Z3 allocation flow with hand-authored allocation tables
   plus collision and consistency validation.
6. Update YAML specs, generators, RTL decode, AGU request shape, assembler, and
   tests after the design is finalized.
