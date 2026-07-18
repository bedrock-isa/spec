# Bedrock ABI documents

The ABI document set is maintained directly in TeX. It follows a four-layer
core stack. The Platform / OS ABI spans and constrains the stack, while the ISA
specification is its non-ABI architectural foundation.

- `bedrock-elf-abi.tex` specifies the layer-1 binary-format ABI.
- `bedrock-c-abi.tex` specifies the layer-2 C language ABI, including ordinary
  and far-pointer representations and calls.

Source-language and compiler-facing contracts are kept outside the ABI stack:

- `../c/bedrock-c-far-extensions.tex` specifies the `__far` C language
  extension and cross-segment source semantics.
- `../c/bedrock-target-intrinsics.tex` specifies compiler builtins and target
  header interfaces.
- `../c/include/` contains the corresponding compiler-facing target headers.
- `../guides/bedrock-programming-toolchain-guide.tex` contains non-normative
  C-library, compiler, and runtime examples.

All reference documents use `../tex/bedrock-reference-common.tex`. The ISA
reference remains generated from the architectural definition and allocation
sources, but its generated TeX inputs the same common component.

The ABI TeX documents are the normative prose sources. The retained ABI
quick-reference tables are generated from `abi_tables.yaml`, whose semantic
fields record return locations, call-relocation relationships, ordinary and
atomic access rules, Bedrock-specific sections, and TLS relocation families.
Run `make abi-tables` after changing that manifest. In addition,
`calling_convention_cases.json` contains compiler-facing call-layout fixtures,
and `../tools/abi_call_model.py` is the executable reference procedure that
checks them. The same case identifiers appear in the worked examples in the C
ABI, so documented coverage and conformance fixtures cannot silently diverge.

Generated assembly included in the C ABI is non-normative. Compiler output for
an unimplemented or nonconforming path is kept out of the reference document.

Run `make validate-docs` to check layer assignments, relocation tables,
generated ABI tables, document boundaries, call-layout fixtures, and
intrinsic/header agreement.
Run `make validate-abi-model` to check only the executable calling-convention
model. Run `make docs` to build the complete six-document reference and guide
set.
