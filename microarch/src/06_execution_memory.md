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
