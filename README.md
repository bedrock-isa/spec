# ISA Design

This repository contains the current Bedrock ISA design sources, opcode
allocation, ABI and compiler-interface specifications, validation tools, and
reference-document outputs.

The active source tree is:

```text
isa/memory_model/             draft formal-validation gate and litmus obligations
isa/defs/SCHEMA.md            frozen versioned YAML document contract
isa/defs/schema.lock          decoder version and SHA-256 contract lock
isa/defs/**/instructions/    instruction.yaml, encodings.yaml, and optional TeX per instruction
isa/reference/architecture_tables.yaml generated ISA-reference table data
isa/tex/*.tex                shared reference-document components
isa/abi/abi_tables.yaml      generated ABI quick-reference table data
isa/abi/bedrock-elf-abi.tex  ELF binary-format ABI source
isa/abi/bedrock-c-abi.tex    C ABI source, including far-pointer ABI
isa/c/target_intrinsics.yaml generated target-intrinsic table data
isa/c/*.tex                  C language-extension and compiler-API sources
isa/c/include/*.h            target intrinsic header interfaces
isa/guides/*.tex             non-normative programming and toolchain guides
isa/tools/validate_defs.py   definition include/family consistency validator
isa/tools/validate_schema.py version-lock and strict YAML decoder gate
isa/tools/validate_alloc.py  allocation collision and cardinality validator
isa/tools/validate_isa.py    definition/allocation join validator
isa/tools/validate_abi_docs.py ABI document and intrinsic-header validator
isa/tools/encoding_architecture.py fixed instruction framing and opcode-class grammar
isa/tools/gen_docs.py        pure reference-document rendering library used by the compiler
isa/tools/latex_to_markdown.py derived Markdown converter for TeX documents
isa/tools/gen_alloc_report.py allocation occupancy report generator
```

Historical source snapshots and reference material are kept under `old/`.

## Instruction Documentation Sources

Each instruction lives in an `instructions/<MNEMONIC>/` directory.
`instruction.yaml` carries the title, summary, one-paragraph description, and
common attributes. `encodings.yaml` owns every concrete encoding form, including
syntax, operands, fields, sizes, and reclaim constraints. Instructions that need
additional normative material name a body-only TeX file with
`additional_description`; the generator supplies the `Detailed Semantics`
heading.

Each instruction-set `instructions.yaml` explicitly lists instruction
directories. Extension-wide architectural metadata lives in an
`extension.yaml`; `extensions.yaml` lists root extension names and each
extension may list its own sub-extensions. The loader traverses that hierarchy
separately from the per-instruction definitions. Each listed directory must
contain an `instruction.yaml` whose `mnemonic` matches the directory name.

## Validation

Install the Python tooling dependency once with:

```sh
python3 -m pip install -r requirements.txt
```

The document compiler runs the definition, allocation, ABI, and cross-source
checks as mandatory stages. Build and validate all six reference documents and
their Markdown derivatives with:

```sh
make docs
```

## Reference Documents

`isa/tools/compile_documents.py` is the only document compilation entry point.
It generates all derived TeX in a temporary build overlay, compiles PDF and
Markdown from that same overlay, validates the results, and publishes them only
after the complete run succeeds. Generated TeX is not tracked in the source
tree.

```sh
make docs
```

`make docs-pdf` and `make docs-markdown` are partial development builds. They
do not replace the complete `make docs` quality gate.

## Allocation Reports

Generate allocation occupancy reports:

```sh
python3 isa/tools/gen_alloc_report.py
```

The report outputs are written under `build/reports/`.
