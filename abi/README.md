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
objects consumed by generators. Authored TeX owns the reader-facing
composition. A generator projects only collections that the artifact contract
explicitly makes public; membership in an internal catalog does not by itself
create a table row, section, label, or anchor. All Bedrock reference documents
share the `bedrock-reference` package under `../style/` for presentation.
