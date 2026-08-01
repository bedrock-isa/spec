# Architectural Introduction

Bedrock is a little-endian, byte-addressed instruction set architecture for general-purpose systems software. It keeps the useful parts of a CISC design—compact common forms, variable-length instructions, rich effective addresses, and selected register–memory and memory–memory operations—while putting firm boundaries around decoding, side effects, faults, and compatibility.

The project treats an ISA as more than an opcode catalog. Its architectural contract extends from programmer-visible state and instruction execution through address translation, memory ordering, privilege, event delivery, binary formats, and the C language interface. The goal is a design that a processor, assembler, compiler, linker, operating system, and conformance tool can interpret independently and still agree on what software observes.

Bedrock is under active design. It is a specification project, not a claim of a frozen production target or a particular microarchitecture.

## Architectural character

### A bounded variable-length CISC core

The integer programming model has sixteen 64-bit general registers, `R0` through `R15`, plus separate `SP` and `PC` registers. Integer operations use byte, word, long, and quad widths of 8, 16, 32, and 64 bits.

Instructions are byte-oriented records with explicit, bounded lengths from 1 to 18 bytes. Short encodings keep common operations compact; longer records carry richer opcodes, operands, displacements, immediates, and descriptors. The complete record boundary is established before operand evaluation begins. This preserves the density and flexibility of a variable-length ISA without making instruction acquisition or exceptional behavior open-ended.

### Expressive operands with a regular structure

An effective-address operand can name a register, immediate, absolute address, or memory location. Memory forms support base and index registers, scaled indexing, displacements, explicit segment selection, `SP`- and `PC`-relative addressing, and pre-decrement or post-increment updates.

These forms share one operand model instead of being redefined instruction by instruction. Compact descriptors cover common cases, while an extended descriptor carries less common combinations. Address calculation, memory access, and register auto-update remain distinct architectural steps, so a rich operand does not imply an ambiguous side effect.

### Layered addressing rather than one flat assumption

Bedrock separates effective-address calculation, segment pre-translation, optional page-table translation, and the final memory-system access. `CS`, `DS`, and `SS` provide fixed code, data, and stack contexts, while `GS0` through `GS5` provide additional explicitly selectable domains. Segment state may be disabled, translated, or used as a bounds-only window.

Paging adds permissions, page geometry, and an address-type distinction. Ordinary byte-addressed memory participates in the coherent memory system; slot-addressed mappings represent acknowledged transactions for device-style access. Keeping these stages separate makes protection domains, far addressing, ordinary virtual memory, and memory-mapped interaction parts of one composable model.

### Precise execution and restartable failure

The common execution model defines which checks happen first, the order in which operands are accessed, and when architectural effects become visible. An ordinary instruction has one commit point unless its own contract explicitly permits partial completion. Destination writes and auto-update effects remain hidden when an earlier fault wins; multi-page stores validate their full range before any destination byte becomes visible.

This precision also applies to control transfers, stack operations, atomics, privilege changes, and architectural events. Exceptional cases are not commentary around the instruction set—they are part of the instruction set.

### A weak memory model with explicit strengthening

Normal memory is coherent and multi-copy atomic, but the baseline ordering between different locations is deliberately weak. Atomic operations provide relaxed, acquire, release, acquire-release, and sequentially consistent modes. Read, write, and cumulative full fences express the ordering that software actually requires.

This gives implementations room to speculate and reorder while giving concurrent software a concrete contract for synchronization. Cache maintenance, translation-cache maintenance, self-modifying code, and slot-addressed transactions are defined in the same ordering model rather than left as unrelated platform folklore.

### Scalar repetition with precise boundaries

`REP`, conditional `REPcc`, and grouped `REPG` execution repeat scalar instructions or bounded instruction groups. They do not introduce a separate vector register model: architectural state changes as if scalar iterations committed in program order.

Each iteration retains ordinary operand and fault rules. When an event interrupts repeated execution, the remaining repeat context is saved and can be restored. The result is a compact streaming mechanism that preserves scalar reasoning, debugging, and restartability.

### System software is part of the architecture

Bedrock has distinct user and supervisor modes. Explicit system calls use a validated supervisor-call state and return bank, while exceptions, interrupts, and NMIs use a separate common architectural-event path. Entry and return transitions validate their complete context and commit atomically, avoiding half-entered privilege states.

The ISA is the foundation of a broader software contract. Bedrock defines a 64-bit ELF environment, an LP64 C ABI, near and far call models, far pointers that pair an address with a segment image, and compiler-facing target operations. These layers are kept separate in meaning, but they are designed together so that an architectural feature has a coherent path into real programs.

### Optional features are discoverable contracts

The base architecture is scalar. Optional groups are discovered through `CPUID`, whose results form a compatibility boundary rather than a performance hint. The floating-point extension adds sixteen 64-bit floating-point registers and its own status state. Approximate transcendental operations are exposed through individually discoverable accuracy contracts with stable identifiers and certified error bounds.

Software can therefore choose an optional facility based on an explicit semantic guarantee and retain a fallback when that guarantee is absent. New capability is meant to arrive as a named, testable contract—not as an encoding that software has to probe by accident.

## Design philosophy

**Programmer-visible semantics come first.** Instruction descriptions begin with state, operands, access order, results, and failure behavior. Encoding is important, but it does not get to define semantics indirectly.

**Complexity must stay bounded.** Variable-length instructions have explicit maximum size. Rich addressing is split into compact and extended forms. Repetition is opt-in and has fixed continuation rules. Optional behavior is enumerated and discoverable.

**Expressiveness must not weaken precision.** Memory operands, auto-update modes, far control flow, and repeated execution are useful only when their commit points, fault priority, and restart behavior are as clear as those of simple register operations.

**Implementation freedom ends at the architectural boundary.** A processor may pipeline, speculate, cache, or reorder internally. It may not change the values, ordering relations, fault identity, or committed state that the contract exposes.

**Compatibility is explicit.** Reserved encodings stay reserved, noncanonical forms are rejected unless deliberately defined, and optional state is gated by discovery. Incompatible semantic changes require a new architectural identity or contract rather than a silent reinterpretation.

**One meaning should serve every layer.** The project uses structured architectural definitions and machine-checkable invariants so that instruction semantics, reference material, ABI rules, and conformance evidence do not drift into parallel versions of the architecture.

**Boundary cases deserve first-class treatment.** Cross-page accesses, failed atomics, nested events, partial repeat progress, cache synchronization, and far-pointer transitions are specification subjects in their own right. The design is judged by how well these cases compose, not only by how elegant the happy path looks.

## Direction

Bedrock is moving toward a complete, implementation-independent systems contract: a stable scalar foundation, carefully scoped optional extensions, precise compatibility rules, and an end-to-end bridge from machine behavior to compiled programs.

The intended evolution is conservative at the base and explicit at the edges. New instructions or state should justify their interaction with decoding, addressing, faults, memory ordering, context switching, ABI representation, and feature discovery. Capabilities that cannot yet make those relationships precise should remain outside the architectural contract.

The long-term measure of success is not the number of instructions. It is whether independent hardware and software implementations can share binaries, survive boundary conditions, and reach the same observable result from the same architectural state. Bedrock aims to make that agreement the architecture's central product.
