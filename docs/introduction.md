# Architectural Introduction

Bedrock is a 64-bit instruction set architecture for general-purpose systems software. Its specification covers programmer-visible state and instruction execution, address translation, memory ordering, privilege, event delivery, binary formats, and the C language interface.

## Architecture overview

### Programming model and instructions

The integer programming model has sixteen 64-bit general registers, `R0` through `R15`, plus separate `SP` and `PC` registers. Integer operations use byte, word, long, and quad widths of 8, 16, 32, and 64 bits. Instructions are byte-oriented records with explicit lengths from 1 to 18 bytes, and the complete record boundary is established before operand evaluation begins.

Effective-address operands can name registers, immediates, absolute addresses, or memory locations. Memory forms support base and index registers, scaled indexing, displacements, explicit segment selection, `SP`- and `PC`-relative addressing, and pre-decrement or post-increment updates. Address calculation, memory access, and register auto-update are distinct architectural steps.

### Addressing and memory

Address processing separates effective-address calculation, segment pre-translation, optional page-table translation, and the final memory-system access. `CS`, `DS`, and `SS` provide code, data, and stack contexts, while `GS0` through `GS5` provide additional selectable domains. Segment state may be disabled, translated, or used as a bounds-only window. Paging adds permissions, page geometry, and an address-type distinction; ordinary byte-addressed memory and slot-addressed mappings have separate access contracts.

Normal memory is coherent and multi-copy atomic, with weak baseline ordering between different locations. Atomic operations provide relaxed, acquire, release, acquire-release, and sequentially consistent modes. Read, write, and cumulative full fences provide explicit ordering. Cache maintenance, translation-cache maintenance, self-modifying code, and slot-addressed transactions participate in the same ordering model.

### Execution and events

The common execution model defines check order, operand access order, and the visibility of architectural effects. An ordinary instruction has one commit point unless its contract explicitly permits partial completion. Destination writes and auto-update effects remain hidden when an earlier fault wins, and multi-page stores validate their full range before any destination byte becomes visible.

`REP`, conditional `REPcc`, and grouped `REPG` execution repeat scalar instructions or bounded instruction groups in program order. Each iteration retains ordinary operand and fault rules. An event saves the remaining repeat context so execution can resume.

Bedrock has distinct user and supervisor modes. Explicit system calls use validated supervisor-call state and a return bank, while exceptions, interrupts, and NMIs use a separate architectural-event path. Entry and return transitions validate their complete context and commit atomically.

### Software interfaces and optional facilities

The software contract includes a 64-bit ELF environment, an LP64 C ABI, and compiler-facing target operations. Optional instruction groups are discovered through `CPUID`, whose results define a compatibility boundary. The floating-point extension adds sixteen 64-bit floating-point registers and status state. Approximate transcendental operations use individually discoverable accuracy contracts with stable identifiers and certified error bounds.
