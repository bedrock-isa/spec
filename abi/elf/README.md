# Bedrock ELF ABI

Collections keep their inventories inside their matching directories, for
example `relocations/relocations.yaml`. `process_entry.yaml` is the singleton
language-independent entry contract. ABI register overlays follow the ISA
register hierarchy under `registers/groups/`; each group owns its DWARF
numbering and register-specific entry declarations. `model/` loads the
hierarchy, parses authored
relocation expressions with the ELF relocation metasyntax, and resolves ISA
and ELF relationships. `documents/` contains normative prose. The `elf-abi`
artifact derives its tables from the typed catalog.

The `llvm-elf-abi` artifact projects the same typed catalog into LLVM/LLD
inputs. It emits the standard `ELF_RELOC` definition file plus a reusable
X-macro catalog containing relocation properties and expressions, relaxation
edges, code models, TLS models, linkage protocols, DWARF register assignments,
and entry-state data. The artifact structurally lowers each parsed relocation
expression to its LLVM/LLD expression class and rejects unsupported expression
shapes during generation.
