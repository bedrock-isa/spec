# Bedrock

**A bounded variable-length CISC ISA focused on precise architectural semantics, streaming scalar execution, and implementation-independent compatibility.**

Bedrock is a draft 64-bit systems architecture. It combines compact instructions and rich addressing with explicit instruction boundaries, precise commit and fault rules, a complete memory model, and a software contract spanning ELF and C.

The project is designed so that processors, compilers, operating systems, and conformance tools can be developed independently and still agree on exactly what software observes.

## Demos

Two emulator demos are already used during development. Recordings have not been published yet.

> **Keyboard echo — video placeholder**  
> Video coming soon.

> **3D renderer — video placeholder**  
> Video coming soon.

## A Bedrock instruction in one glance

```asm
REP R1, ADD.Q [DS:R2 + R3++ * 8 + 32], R4
```

Repeat the scalar `ADD.Q` body `R1` times: add the 64-bit value at `DS:(R2 + R3 * 8 + 32)` to `R4`, increment the element index `R3` after every committed iteration, and retain a precise restart boundary if an iteration faults.

This small example captures several Bedrock ideas at once: segment-qualified indexed-indirect addressing, Q-width scaling, displacement, post-increment, scalar repetition, and iteration-level commit semantics.

## What makes Bedrock distinct

- **Bounded variable-length encoding.** Instructions occupy 1 to 18 bytes. Common operations stay compact, while richer records remain explicitly framed before operand evaluation begins.

- **Structured CISC operands.** Register, immediate, absolute, indexed, segment-qualified, `SP`-relative, `PC`-relative, and auto-update forms share one effective-address model instead of accumulating instruction-specific exceptions.

- **Precise architectural effects.** Access order, fault priority, destination visibility, and commit points are part of the contract. Rich operands and control flow do not get weaker failure semantics.

- **Streaming without hidden vector state.** `REP`, conditional `REPcc`, and grouped `REPG` repeat scalar work in program order. Events preserve the remaining repeat context, so execution stays debuggable and restartable.

- **A complete systems boundary.** Segment pre-translation, optional paging, coherent weakly ordered memory, atomics, fences, privilege transitions, event delivery, ELF, and the LP64 C ABI are designed as related layers.

- **Explicit evolution.** Optional facilities are discovered through `CPUID`; reserved encodings stay reserved; incompatible behavior receives a new architectural identity or contract instead of silently changing meaning.

Bedrock is still evolving, but the direction is deliberate: keep the scalar foundation stable, make extensions discoverable, and require every feature to explain its interactions with decoding, faults, memory ordering, context switching, and software interfaces.

For the longer explanation of the architecture and its design philosophy, read the [Architectural Introduction](docs/introduction.md).
