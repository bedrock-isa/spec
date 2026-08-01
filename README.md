# Bedrock ISA

[![CI](https://github.com/kms1212/bedrock-isa/actions/workflows/ci.yml/badge.svg)](https://github.com/kms1212/bedrock-isa/actions/workflows/ci.yml)

Bedrock is an in-development, bounded, byte-addressed CISC instruction set
architecture. This repository contains the architecture definitions, normative
reference material, ABI contracts, C-facing interfaces, conformance data, and
the compiler that turns those sources into a consistent document set.

> [!WARNING]
> Bedrock is currently an unreleased draft. No architecture revision has been
> assigned, and encodings, interfaces, and behavior may change without backward
> compatibility. Do not treat the current specification as a stable deployment
> target.

## Architecture at a glance

- Sixteen 64-bit integer registers, with separate stack-pointer and
  program-counter state
- Explicit instruction lengths from 1 to 18 bytes
- Byte, word, long, and quad integer operation sizes
- Register, memory, immediate, absolute, indexed, segment-qualified, and
  auto-update effective-address forms
- Segment pre-translation followed by optional page-table translation
- User and supervisor execution modes
- An optional floating-point extension and an optional approximate
  transcendental extension

## Document set

`make docs` compiles and validates five coordinated documents:

| Document | Scope | PDF output |
| --- | --- | --- |
| Programmer's Reference Manual | Architectural state, encoding, execution, memory, events, conformance, and instruction definitions | `build/isa_reference.pdf` |
| [Bedrock ELF ABI](isa/abi/bedrock-elf-abi.tex) | ELF objects, linking, relocation, loading, dynamic linking, TLS metadata, and code models | `build/latex/bedrock-elf-abi/bedrock-elf-abi.pdf` |
| [Bedrock C ABI](isa/abi/bedrock-c-abi.tex) | C data model, register convention, calling convention, stack, unwind, and memory-model mapping | `build/latex/bedrock-c-abi/bedrock-c-abi.pdf` |
| [C far-pointer extensions](isa/c/bedrock-c-far-extensions.tex) | Bedrock-specific C types and source-language semantics for far pointers | `build/latex/bedrock-c-far-extensions/bedrock-c-far-extensions.pdf` |
| [Target intrinsics](isa/c/bedrock-target-intrinsics.tex) | Compiler builtins, intrinsic headers, signatures, and effects | `build/latex/bedrock-target-intrinsics/bedrock-target-intrinsics.pdf` |

The complete local build also writes Markdown counterparts to
`build/isa_reference.md` and `build/markdown/`. These Markdown files are not
published as CI artifacts.

The Programmer's Reference Manual is assembled from the definitions under
[`isa/defs`](isa/defs), the architecture data under
[`isa/reference`](isa/reference), and the LaTeX templates under
[`isa/tools/latex_builder/templates`](isa/tools/latex_builder/templates).

## Downloading CI artifacts

Every successful push or pull-request build publishes each of the five PDFs as a
separate, directly downloadable artifact from the
[CI workflow](https://github.com/kms1212/bedrock-isa/actions/workflows/ci.yml).
Artifact names match the PDF filenames shown in the table above. Markdown
output, the compiler report, intermediate TeX files, and compiler logs are not
published as artifacts.

To download a document, sign in to GitHub, open a successful workflow run, and
select the desired PDF in the **Artifacts** section of the run summary.
Availability follows the repository's GitHub Actions artifact-retention policy.

## Building the documentation

The CI baseline is Python 3.11 on Ubuntu. A complete local build also needs:

- the Python packages in [`requirements.txt`](requirements.txt);
- `latexmk` and a LaTeX installation with the recommended, base, and extra
  packages used by the documents;
- `pandoc` and `latexpand` for Markdown generation; and
- Poppler's `pdfinfo` and `pdffonts` for PDF verification.

On Debian or Ubuntu, install the non-Python dependencies with:

```sh
sudo apt-get update
sudo apt-get install -y \
  latexmk \
  pandoc \
  poppler-utils \
  texlive-fonts-recommended \
  texlive-latex-base \
  texlive-latex-extra \
  texlive-extra-utils
```

Then clone and build the repository:

```sh
git clone https://github.com/kms1212/bedrock-isa.git
cd bedrock-isa

python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt

make docs
```

The generated document set is written to `build/`; CI publishes only its PDF
subset. The compiler stages all outputs before publishing them and refuses to
complete if generation changes a tracked source file.

For iteration, the following partial targets are available:

```sh
make docs-pdf       # PDF documents only
make docs-markdown  # Markdown documents only
```

Partial targets are development aids. `make docs` is the complete repository
quality gate.

## What the quality gate checks

The document compiler performs the full validation and generation pipeline in
one command:

1. validates the frozen YAML schema and all architecture definitions;
2. checks encoding allocation, joined ISA semantics, ABI/compiler interfaces,
   conformance vectors, and cross-document navigation;
3. derives architecture, ABI, intrinsic, effective-address, and instruction
   artifacts from their canonical definitions;
4. compiles every PDF and Markdown document;
5. rejects undefined references, missing glyphs, overfull boxes, duplicate PDF
   destinations, and other forbidden LaTeX diagnostics; and
6. verifies that every PDF is readable and uses embedded fonts.

A machine-readable build report is written to
`build/document-compile.json`.

## Repository layout

```text
isa/
├── defs/          Instruction, operand, register, size, and extension definitions
├── reference/     Architecture tables, navigation data, and conformance vectors
├── memory_model/  Memory-order and cache-synchronization litmus data
├── abi/           C and ELF ABI sources and executable ABI reference data
├── c/             C extensions, target intrinsics, and public intrinsic headers
├── tex/           Shared document style and LaTeX infrastructure
└── tools/         Schema, validation, generation, and document compiler code
```

## Working on the specification

The repository deliberately separates semantic definitions from rendered
documents:

- edit instruction semantics and encodings in the relevant files under
  `isa/defs/`;
- edit shared architectural prose and layout in
  `isa/tools/latex_builder/templates/`;
- edit ABI and C-interface prose in the corresponding `isa/abi/` and `isa/c/`
  sources;
- treat [`isa/defs/SCHEMA.md`](isa/defs/SCHEMA.md) and
  `isa/defs/schema.lock` as a coordinated, frozen schema contract; and
- do not hand-edit or commit files under `build/`. Generated TeX exists only in
  the build overlay and must have a source-document consumer.

Before submitting a change, run:

```sh
make docs
```

For visual or layout changes, inspect the final PDFs as well as the build
result. A successful compilation proves structural consistency, not visual
correctness.

## License

This repository does not currently include a license. Public availability does
not grant permission to copy, modify, or redistribute the work.
