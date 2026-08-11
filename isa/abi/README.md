# Bedrock ABI documents

The two ABI documents are maintained directly in TeX:

- `bedrock-elf-abi.tex` specifies the ELF object, linking, and loading ABI.
- `bedrock-c-abi.tex` specifies the C language binding and calling convention.

Source-language and compiler-facing contracts are kept separately:

- `../c/bedrock-target-intrinsics.tex` specifies compiler builtins and target
  header interfaces.
- `../c/include/` contains the corresponding compiler-facing target headers.

All reference documents use `../tex/bedrock-reference-common.tex`. The ISA
reference remains generated from the architectural definition and allocation
sources, but its generated TeX inputs the same common component.

The ABI TeX documents are the normative prose sources. The ABI quick-reference
tables are generated from `abi_tables.yaml`, whose semantic
fields record return locations, call-relocation relationships, ordinary and
atomic access rules, and TLS relocation families.
The document compiler renders those tables in its build overlay. In addition,
`calling_convention_cases.json` contains compiler-facing call-layout cases,
and `../tools/abi_call_model.py` is the executable reference procedure that
checks them. Worked examples reference those cases through a TeX macro that
rejects unknown or missing documented IDs during compilation.

Generated assembly included in the C ABI is non-normative. Compiler output for
an unimplemented or nonconforming path is kept out of the reference document.

Run `make docs` to check the semantic sources and build the complete
four-document PDF and Markdown set. No partial validation target is a quality
gate.
