# Bedrock SystemVerilog RTL

This directory contains hand-written SystemVerilog RTL for Bedrock.

Directory layout:

- `common/`: shared packages, typedefs, and bitfield helpers.
- `dolomite0/`: Dolomite0 baseline scalar pipeline packages and future core integration RTL.
- `frontend/`: instruction-fetch and decode-front-end RTL.
- `execute/`: hand-written shared execute-stage helper units.
- `tb/`: SystemVerilog testbenches.

Instruction word 0 carries the prefix-present bit, encoded instruction length,
and 12-bit primary payload directly. The shared `bedrock_pkg` bitfield helpers
are the RTL source of truth for those slices; there is no separate predecode
stage for discovering instruction length.

`bedrock_full_decode` decodes one instruction window into a normalized record:
word-0 length, prefix state, instruction form, extracted operand fields, up to
two decoded EA operands, AGU request records for those operands, repeat-prefix
legality, and the minimum required word count including EA payload words.

`bedrock_agu` is a hand-written shared address-generation unit. It consumes a
decoded AGU request plus operand register values and payload data, then produces
the effective address and optional address-update writeback value. The generated
ISA decode snippets stop at EA classification and request construction; address
arithmetic remains common RTL rather than spec-generated RTL.

`dolomite0/bedrock_core_pkg.sv` names the Dolomite0 baseline scalar pipeline
stages used by the microarchitecture document:

```text
F0 -> F1 -> P0 -> D0 -> R0 -> X0 -> X1 -> M0 -> W0
```

The initial core is single-issue and in-order. `X1` is kept as the explicit
translation boundary even before segment and paging translation are implemented.
This RTL target is the `Dolomite0` implementation profile: no branch predictor,
out-of-order machinery, FPU datapath, SIMD datapath, uop cache, or REPG-fast
folding.

The integrated decode RTL uses typed SystemVerilog packages for lint and
simulation. The Yosys synthesis target lowers that same source path through
`sv2v` before reading it into Yosys, so the synthesized logic follows the
integration RTL instead of a duplicate package-free wrapper.

Useful targets:

```sh
make -C rtl lint
make -C rtl test
make -C rtl decode-test
make -C rtl execute-test
```

From the repository root, the generic dispatcher can run the same targets:

```sh
make rtl TARGET=lint
make rtl TARGET=test
make rtl TARGET=decode-test
make rtl TARGET=execute-test
```

Generated Verilator artifacts are written under `build/verilator/`.
