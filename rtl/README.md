# Bedrock SystemVerilog RTL

This directory contains hand-written SystemVerilog RTL for Bedrock.

Directory layout:

- `common/`: shared packages, typedefs, and bitfield helpers.
- `dolomite0/`: Dolomite0 baseline scalar pipeline packages and future core integration RTL.
- `frontend/`: instruction-fetch and decode-front-end RTL.
- `execute/`: hand-written shared execute-stage helper units.
- `tb/`: SystemVerilog testbenches.

The initial RTL boundary is the instruction word-0 predecoder and the
line-wide predecoder built from it:

- extracts the prefix-present bit,
- extracts the encoded instruction length,
- computes the total instruction length in 16-bit words,
- extracts the 12-bit primary payload,
- identifies the HALT and ILLEGAL sentinel payloads.

`bedrock_line_predecode` applies the same word-0 predecode in parallel across a
64-byte / 32-word fetch or grouping window. It does not decide instruction
starts or slot placement; later frontend logic can walk the explicit word-0
lengths and select the instruction-start words it wants to fully decode.

`bedrock_line_entry_precheck` uses that line view together with the generated
instruction and prefix decoders. For every possible word entry point, it checks
the optional prefix word, picks the extension word after the prefix when the
decoded primary payload needs one, and reports REPcc/REPG validity for the
decoded form.

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

The integrated entry precheck uses typed SystemVerilog packages for lint and
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
