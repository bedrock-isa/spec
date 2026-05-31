# Bedrock ISA Design

Bedrock is a draft instruction-set architecture and tooling workspace for a
bounded, 16-bit-word-oriented CISC design. The repository contains the
declarative ISA specification, allocation and validation tools, generated
assembler/disassembler infrastructure, a Bedrock QBE backend experiment, RTL
frontend/execute helper work, and microarchitecture notes.

The architecture is still evolving. The YAML specification under `isa/spec/`
is intended to be the source of truth; generated files are written under
`build/` and are not tracked.

## Repository Layout

- `isa/spec/`: declarative ISA, ABI, C ABI, register, prefix, EA, and semantic
  descriptions.
- `isa/tools/`: validators, opcode allocator, documentation generators, SLEIGH
  generator, C assembler/disassembler table generator, and RTL decode
  generators.
- `isa/asm/`: standalone Bedrock ELF assembler support code.
- `qbe/`: vendored QBE tree with the experimental Bedrock target backend.
- `benchmarks/arch_compare/`: small code-density comparison kernels.
- `tools/compare_arch.py`: cross-target code-density comparison runner.
- `rtl/`: SystemVerilog decode/predecode/AGU and execute helper experiments.
- `microarch/`: source fragments for implementation-oriented design notes.

## Common Commands

```sh
make validate
make allocation
make asm-disasm-smoke
make qbe-bedrock
make arch-compare
```

Optional document and RTL flows:

```sh
make manual-pdf
make abi-all-pdf-final
make rtl-test
```

## Prerequisites

Core tooling:

- Python 3
- Python packages from `requirements.txt`
- a C compiler and `make`

```sh
python3 -m pip install -r requirements.txt
```

Optional flows use additional tools:

- `latexmk`/`pdflatex` for generated PDF manuals
- Verilator/Yosys for RTL lint, tests, and synthesis reports
- cross compilers or Clang targets for architecture code-density comparisons

## Generated And Local Files

`build/`, `outputs/`, local PDFs, Python caches, and local compiler products are
ignored. Reference PDFs used during design are not part of the repository; keep
them outside version control or add them locally as needed.

## License

No repository-wide license has been selected yet. The vendored QBE sources in
`qbe/` retain their own license in `qbe/LICENSE`.
