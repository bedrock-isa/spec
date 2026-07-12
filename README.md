# ISA Design

This repository contains the current Bedrock ISA design sources, opcode
allocation, ABI and compiler-interface specifications, validation tools, and
reference-document outputs.

The active source tree is:

```text
docs/isa_architectural_state_recovery_plan.md
                              architectural-state migration recovery plan
isa/defs/*.yaml              instruction semantics and architectural definitions
isa/alloc/*.yaml             opcode allocation source of truth
isa/tex/*.tex                shared reference-document components
isa/abi/bedrock-elf-abi.tex  ELF binary-format ABI source
isa/abi/bedrock-c-abi.tex    C ABI source, including far-pointer ABI
isa/c/*.tex                  C language-extension and compiler-API sources
isa/c/include/*.h            target intrinsic header interfaces
isa/tools/validate_defs.py   definition include/family consistency validator
isa/tools/validate_alloc.py  allocation collision and cardinality validator
isa/tools/validate_isa.py    definition/allocation join validator
isa/tools/validate_abi_docs.py ABI document and intrinsic-header validator
isa/tools/gen_docs.py        reference document generator
isa/tools/latex_to_markdown.py derived Markdown converter for TeX documents
isa/tools/gen_alloc_report.py allocation occupancy report generator
```

Historical source snapshots and reference material are kept under `old/`.

## Validation

Install the Python tooling dependency once with:

```sh
python3 -m pip install -r requirements.txt
```

Run the definition and allocation checks with:

```sh
python3 isa/tools/validate_defs.py
python3 isa/tools/validate_alloc.py isa/alloc/*.yaml
python3 isa/tools/validate_isa.py
python3 isa/tools/validate_abi_docs.py
```

## Reference Documents

Generate the ISA reference TeX source:

```sh
python3 isa/tools/gen_docs.py -o build/isa_reference.tex
```

Generate derived GitHub-Flavored Markdown with Pandoc:

```sh
python3 isa/tools/gen_docs.py --format markdown -o build/isa_reference.md
```

The Markdown file is generated from the fully rendered LaTeX document. It is a
publication artifact, not a second documentation source. No Markdown templates
are maintained in the repository. Install Pandoc first, or set the `PANDOC`
environment variable to its executable path.

The directly maintained ABI and compiler-interface TeX documents use the same
converter. For example:

```sh
python3 isa/tools/latex_to_markdown.py \
  isa/abi/bedrock-elf-abi.tex \
  build/markdown/bedrock-elf-abi.md
python3 isa/tools/latex_to_markdown.py \
  isa/abi/bedrock-c-abi.tex \
  build/markdown/bedrock-c-abi.md
```

Build the PDF from the generated TeX:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build build/isa_reference.tex
cp build/isa_reference.pdf isa_reference.pdf
```

Build all five reference documents:

```sh
make docs
```

The four directly maintained TeX documents can be built independently with
`make elf-abi`, `make c-abi`, `make c-far-extensions`, and
`make target-intrinsics`.

Use `make isa-reference-markdown` for the ISA reference, `make abi-markdown`
for both ABI documents, or `make docs-markdown` for all five derived Markdown
artifacts.

## Allocation Reports

Generate allocation occupancy reports:

```sh
python3 isa/tools/gen_alloc_report.py
```

The report outputs are written under `build/reports/`.
