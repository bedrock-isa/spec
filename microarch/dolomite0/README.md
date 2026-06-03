# Bedrock Microarchitecture

This document records the working microarchitecture model for Bedrock
implementations. It is not the architectural ISA reference. Architectural
software-visible behavior remains defined by the ISA, ABI, and C ABI documents.

The goal of this document is to keep RTL work guided by an explicit
implementation shape before the core grows beyond small predecode blocks.

## Design Intent

Bedrock is a bounded, 16-bit-word-oriented CISC ISA. The implementation should
take advantage of properties that are architecturally simple:

- word 0 always contains prefix-present, length, and primary payload fields,
- instruction length is known from word 0 alone,
- instruction size is bounded to eight 16-bit words,
- prefix count is bounded,
- effective-address forms are declarative and finite,
- repeat forms are explicit rather than inferred from opaque loops.

The first RTL target is the `Dolomite0` implementation profile: a clear
in-order integer reference core. It is not an out-of-order design, does not
include an FPU, and does not fold grouped repeat streams into internal SIMD
operations.

Initial implementation scope:

- in-order fetch, decode, issue, execution, and retirement,
- integer, branch/control, load/store, AGU, multiply/divide, and system-control
  execution units,
- scalar `REP`, `REPcc`, and `REPG` execution,
- precise exceptions by retiring architectural state in program order,
- no register renaming, reorder buffer, speculative out-of-order issue, FPU
  datapath, or SIMD/streaming folding.

The design should keep interfaces clean enough that a later high-performance
core can add predecode metadata, uop caching, renaming, out-of-order issue, an
FPU, or internal streaming execution without changing the architectural model.

## Implementation Profile Dolomite0

The initial RTL target implements the `Dolomite0` profile: a baseline scalar
Bedrock core intended to validate the ISA frontend, integer execution, precise
state updates, and repeat semantics before high-performance machinery is added.

`Dolomite0` is an implementation profile, not an ISA profile. It describes what
the current RTL is expected to implement and what it intentionally leaves out.
The name follows the Bedrock geology theme: Dolomite is a relatively low-
hardness mineral/rock association, matching a simple but nontrivial baseline
core.

### Dolomite0 Included Features

| Area | Dolomite0 behavior |
| --- | --- |
| Issue model | single issue |
| Execution order | in order |
| Retirement | in order, precise architectural commit |
| Frontend | explicit-length fetch, word-0 predecode, full decode |
| Integer execution | integer ALU, flags, shifts, multiply/divide |
| Address generation | generated EA decode plus shared AGU |
| Memory execution | ordered scalar load/store path |
| Branch/control | resolved by the scalar pipeline, no branch predictor |
| Repeat execution | scalar `REP`, `REPcc`, and `REPG-general` |
| Translation boundary | explicit `X1` stage; initial RTL may pass EA through |
| System control | minimal control-state path sufficient for privileged smoke tests |

### Dolomite0 Excluded Features

| Area | Exclusion |
| --- | --- |
| Branch prediction | no dynamic or static predictor state |
| Speculative execution | no speculative side-effecting execution beyond the current in-order instruction stream |
| Out-of-order execution | no rename, issue queues, load/store queue, or reorder buffer |
| FPU execution | no floating-point datapath |
| SIMD execution | no dedicated SIMD datapath |
| REPG-fast | no grouped-repeat SIMD or streaming folding |
| Uop cache | no decoded-uop cache |
| Multi-issue frontend | no parallel issue or superscalar dispatch |

The profile still keeps the pipeline boundaries needed by later implementations:
`F0`, `F1`, `P0`, `D0`, `R0`, `X0`, `X1`, `M0`, and `W0`. A future profile may
reuse those boundaries while adding branch prediction, wider decode, FPU
execution, out-of-order scheduling, or REPG-fast execution.

## Pipeline Overview

The baseline pipeline is a single-issue, in-order scalar pipeline organized
around explicit instruction packets:

```text
F0  fetch address
F1  fetch window
P0  word-0 and line predecode
D0  full instruction decode
R0  register read and payload gather
X0  integer execute and AGU
X1  translation and memory request
M0  memory access
W0  writeback and commit
```

The baseline core is in-order from issue through retirement. Execution may use
multi-cycle units, but architectural state is updated only at defined retirement
points. A simple scoreboard may hold issue until source operands and structural
resources are available; it does not imply register renaming or out-of-order
execution.

### Baseline Stage Boundaries

| Stage | Name | Responsibility |
| --- | --- | --- |
| `F0` | Fetch Address | Select the next fetch PC from sequential flow, redirects, exception entry, or return from a flushed path. |
| `F1` | Fetch Window | Read an aligned instruction fetch window. The initial RTL uses the same 64-byte window size used by grouping-window rules. |
| `P0` | Predecode | Extract word-0 length metadata, prefix-present state, primary payload, sentinel class, and possible entry-point metadata. |
| `D0` | Full Decode | Decode primary and extended opcodes, decode prefixes, classify operands, decode EA fields, and construct normalized instruction records. |
| `R0` | Register Read | Read architectural register operands and gather immediate, displacement, descriptor, and overlong payload words needed by the instruction. |
| `X0` | Execute / AGU | Run integer ALU operations, evaluate branch conditions, form effective addresses, and prepare memory requests. |
| `X1` | Translation / Memory Request | Apply segment and page translation. The initial RTL keeps this stage as an EA pass-through boundary. |
| `M0` | Memory Access | Perform ordered loads, stores, and atomic read-modify-write micro-steps against the memory interface. |
| `W0` | Writeback / Commit | Commit register writes, flag writes, PC updates, memory side effects, and precise exception state in program order. |

These stage names are architectural implementation names, not ISA-visible
state. They are used so the RTL, testbenches, and microarchitecture document can
refer to the same pipeline boundaries.

### Multi-Cycle Instructions

Bedrock instructions may decompose into multiple internal micro-steps. A
register-register integer operation can complete through `X0` and `W0`, while a
register-memory operation normally uses `X0`, `X1`, `M0`, and `W0`. A
memory-memory operation is still one architectural instruction, but internally
it executes ordered source-address, load, destination-address, and store
micro-steps.

The initial pipeline therefore treats `D0` output as an architectural
instruction record plus a small micro-step controller, rather than assuming that
every instruction has exactly one execute cycle.

### Pipeline Control Contract

Each pipeline boundary carries:

- a valid bit,
- the architectural instruction PC,
- the decoded instruction length,
- the current architectural instruction identity,
- any exception or replay metadata raised before the next boundary.

Backpressure is allowed between all stages. A stage may hold its input when a
multi-cycle unit, load/store operation, repeat engine, or future translation
pipeline is busy. A flush clears younger stage state after a branch redirect,
exception, interrupt entry, or other control-flow redirect.

Later high-performance implementations may keep the same logical boundaries
while adding more aggressive machinery:

```text
fetch block
  -> predecode metadata
  -> instruction packet queue
  -> uop translation/cache
  -> rename
  -> issue queues
  -> execution clusters
  -> reorder buffer retirement
```

That path is explicitly outside the initial RTL scope.

The important invariant is that fetch and decode produce a precise linear stream
of architectural instruction instances, even when later implementation stages
execute internally in a different order.

## Frontend and Word-0 Predecode

Word 0 is the natural frontend boundary. The predecoder extracts:

- `P`, the prefix-present bit,
- `L`, the encoded instruction length,
- total instruction length in words,
- the 12-bit primary payload,
- HALT and ILLEGAL sentinel payloads.

Instruction boundaries are computed without walking operand encodings. This
keeps fetch simple even when an instruction contains an extended EA descriptor or
overlong padding.

The frontend should produce an instruction packet containing at least:

```text
pc
word0
length_words
prefix_present
prefix_word_valid
prefix_word
payload_words
primary_payload
sentinel_class
```

Later implementations may cache predecode metadata beside instruction memory:

- instruction start,
- instruction length,
- prefix-present,
- branch/control hint,
- extended descriptor hint,
- REPG start or ENDG hint.

These hints are implementation metadata only. They must be recoverable from the
architectural instruction stream.

## Decode and Uop Translation

The decoder maps architectural instructions into a small internal uop language.
The baseline implementation may execute these uops immediately, while a later
core may queue or rename them.

Typical examples:

```text
MOV.L [A0 + D1 * 4], D0
  -> AGU
  -> LOAD
  -> WRITE_REG

ADD.L [A0], D1
  -> AGU
  -> LOAD
  -> ALU_ADD
  -> WRITE_REG
  -> WRITE_FLAGS

MOV.L D0, [A1]
  -> AGU
  -> STORE

MOV.L [src], [dst]
  -> AGU_SRC
  -> LOAD
  -> AGU_DST
  -> STORE
```

Memory-memory instructions remain architectural instructions, but internally
they are decomposed into ordered uops. The decoder must preserve instruction
identity so exceptions report the architectural instruction and, for repeat
forms, the dynamic instruction instance within the repeated stream.

## Effective Address and Translation Boundary

Effective-address calculation and address translation are separate concerns.

```text
EA decode
  -> base/index/displacement calculation
  -> architectural EA
  -> segment pre-translation
  -> linear address
  -> optional page translation
  -> memory-system address
```

The AGU owns architectural EA calculation:

- register-direct EA selection,
- base register selection,
- D-register index selection,
- index sign-extension mode,
- scale application,
- displacement addition,
- immediate and absolute payload collection.

The memory translation block owns:

- segment selection,
- disabled/translated/bounds-only segment behavior,
- canonical checking when paging is enabled,
- TLB lookup and page-table walk,
- PTE permission checks,
- memory-system address production.

This split keeps integer address arithmetic testable before the MMU is complete
and gives a later implementation room for multiple AGUs feeding a shared
translation pipeline.

## Execution and Memory System

The initial scalar core should contain:

- one integer ALU,
- one branch/control unit,
- one AGU,
- one load/store pipeline,
- one multi-cycle multiply/divide unit,
- one control-register/system unit.

The initial core does not implement the floating-point datapath. Floating-point
architectural state and instruction encodings remain part of the ISA, but this
microarchitecture treats them as an unavailable extension until a later FPU
block is added.

The baseline memory pipeline is ordered. Loads and stores observe architectural
program order unless an explicit later implementation proves that reordering is
invisible under the ISA memory model.

The memory system should distinguish:

- normal memory,
- externally acknowledged or bus-sized memory,
- instruction fetch,
- data load,
- data store,
- page-table walk.

Aligned 1/2/4/8-byte normal-memory accesses are the natural tear-free and
lock-free-atomic implementation boundary. Wider atomics should route through
helper mechanisms unless a later implementation explicitly adds wider atomic
hardware.

## Repeat Engines

### REP and REPcc

`REP` and `REPcc` are best implemented as a repeat uop generator. The repeated
instruction is decoded once, then issued repeatedly while the counter and
condition remain active.

The counter update, condition observation, and fault behavior must match the ISA
definition. Completed iterations commit; a faulting iteration does not commit
the faulting instruction.

### REPG

`REPG` forms a bounded group of ordinary instructions terminated by `ENDG`.
Grouping is a decode/control structure, not a license to change architectural
retirement order.

The architectural dynamic stream is the scalar linearization of the group:

```text
iter0.op0, iter0.op1, ..., iter0.opN,
iter1.op0, iter1.op1, ..., iter1.opN,
...
```

REPG retirement is precise over that linearized stream. On a fault, all dynamic
instruction instances before the faulting instance in that order are committed.
The faulting instance and all later instances are not committed.

The initial core executes `REPG` as this scalar linearized stream. It does not
perform SIMD folding, vectorization, chunked fast execution, or internal
streaming recognition.

`REPG-general` is therefore the only repeat-group execution class implemented by
the first RTL core. The architectural `REPG-fast` continuation class is kept as
a future implementation option, but no fast chunk state is produced by the
initial core.

`REPGF` is an assembler-only contract marker for the fast class. It emits the
same bytes as `REPG`, but the assembler rejects the group if it can see a
fast-class violation such as a selected-counter write, forbidden instruction
class, nested repeat, PC-relative addressing, or grouping-window overflow. The
initial frontend still executes the encoded group through the scalar
`REPG-general` path; `REPGF` is a source-level proof obligation, not an
execution mandate.

Useful implementation strategies include:

- expanding the grouped stream into scalar dynamic instruction instances,
- sharing ordinary integer, AGU, and load/store units with non-repeat code,
- committing completed scalar grouped instructions in architectural order.

Future implementations that add `REPG-fast` or SIMD/streaming folding must still
preserve the scalar linearization as the architectural reference behavior.

## Retirement and Exceptions

The baseline core retires architectural state in program order. This makes
precise exceptions straightforward and gives a clear reference model for later
implementations.

Retirement rules:

- ordinary instructions retire as one architectural instruction,
- decomposed uops retire under their parent architectural instruction,
- stores become globally visible only after their fault checks have passed,
- `REP` retires completed iterations before a faulting iteration,
- `REPG` retires the scalar prefix of the linearized grouped stream.

Exception reporting must preserve enough information to restart or emulate the
faulting architectural operation according to the ISA. For grouped repeat faults,
the saved state identifies the faulting instruction instance and reconstructs
the group start using the architectural repeat-fault continuation fields.
`FAULT_AUX.repeat_kind` distinguishes ordinary `REP`/`REPcc`, `REPG-general`,
and `REPG-fast` continuation records. The initial core only produces ordinary
`REP`/`REPcc` and `REPG-general` records; `REPG-fast` is reserved for a future
implementation that actually performs fast grouped execution.

## Initial RTL Core Plan

The first implementation follows the `Dolomite0` profile and should grow in
small, testable blocks:

1. word-0 predecode,
2. instruction boundary scanner,
3. prefix word collection,
4. instruction packet queue,
5. primary compact decoder skeleton,
6. EA decoder and AGU for register and simple memory forms,
7. integer ALU and flags,
8. load/store path with a simple memory model,
9. branch/control transfer support,
10. REP scalar engine,
11. REPG-general scalar engine,
12. segment and paging translation.

Explicitly out of scope for the initial RTL core:

- out-of-order issue and retirement,
- register renaming and a reorder buffer,
- FPU execution,
- SIMD execution units,
- REPG-fast or SIMD/streaming folding.

The current RTL seed covers the first decode-front-end blocks and has started
the shared integer address-generation path. The next useful blocks are the
integer ALU/flags path and a simple ordered load/store path, because they let the
existing full decoder and AGU feed real architectural execution.
