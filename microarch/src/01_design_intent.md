## Design Intent

Bedrock is a bounded, 16-bit-word-oriented CISC ISA. The implementation should
take advantage of properties that are architecturally simple:

- word 0 always contains prefix-present, length, and primary payload fields,
- instruction length is known from word 0 alone,
- instruction size is bounded to eight 16-bit words,
- prefix count is bounded,
- effective-address forms are declarative and finite,
- repeat forms are explicit rather than inferred from opaque loops.

The first RTL target is a clear in-order integer reference core. It is not an
out-of-order design, does not include an FPU, and does not fold grouped repeat
streams into internal SIMD operations.

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
