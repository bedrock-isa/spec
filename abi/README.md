# Bedrock ABI domains

ABI sources form peer domains beside the ISA:

- `elf/` owns the ELF object, linking, loading, relocation, dynamic-linking,
  and TLS contract.
- `c/` owns the C data model, calling convention, compiler-runtime helpers,
  memory-order lowering, and call-layout projection.

`../interfaces/c/` owns compiler builtins and target headers as source-language
interfaces. `../artifacts/elf-abi/` and `../artifacts/c-abi/` own reader-facing
outputs.

Each domain declares closed inventories in YAML and stores every member in a
matching child directory. Typed projects validate references and provide the
objects consumed by generators. Authored TeX supplies normative prose, while
generated tables project catalog data. All Bedrock reference documents share
`../artifacts/_shared/latex/bedrock-reference-common.tex` for presentation.
