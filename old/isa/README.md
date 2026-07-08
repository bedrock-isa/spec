# ISA Tooling Infrastructure

This directory is the declarative source of truth for the evolving ISA.

## Layout

- `spec/`: YAML architecture description files. `instructions.yaml` owns the
  instruction form catalogs and `operation_semantics` details; `semantics.yaml`
  keeps shared fields and cross-cutting semantic rules. Instruction opcode
  placements are generated, not stored as hand-authored patterns.
- `tools/validate.py`: validates pattern syntax, field widths, length bounds, prefix references, reserved-space collisions, and intentional overlaps.
- `tools/gen_tables.py`: generates optional validated-pattern opcode maps.
- `tools/gen_instruction_tables.py`: generates instruction, operand, and EA
  encoding summary tables from the Z3 allocation result.
- `tools/gen_instruction_specs.py`: generates the per-instruction semantic and
  encoding reference document from `operation_semantics`, the instruction
  catalog, and the allocation result.
- `tools/decodegen.py`: generates decoder metadata JSON.
- `tools/encodegen.py`: generates encoder metadata JSON and canonicalization inputs.
- `tools/gen_sleigh.py`: emits the Ghidra SLEIGH specification from the
  allocation result and the instruction `pcode` semantic bodies.
- `tools/alloc_z3.py`: validates allocator inputs, checks semantic/spec
  alignment, generates operand-field layouts from semantic operands, and uses
  Z3 to choose between one-word primary encodings and generated extended-opcode
  descriptor forms. It generates natural primary extension roots from semantic
  families and operand layouts, while preserving primary headroom for later
  growth. Instruction-owned fixed encodings remain explicit; generated opcode
  placements do not.
- `../build/generated/`: generated artifacts derived from `spec/`.
- `tests/`: reserved for decode, encode, canonicalization, and overlap regression cases.

## Common Commands

Common Make targets:

```sh
make -C isa validate
make -C isa allocation
make -C isa opcode-map
make -C isa sleigh
make -C isa asm-disasm-smoke
make -C isa decode-sv
```

The same targets can be run from this directory without `-C isa`.

The LaTeX manual can be built through the ISA Makefile:

```sh
make -C isa manual-pdf
make -C isa manual-pdf-final
```

Use `manual-pdf-final` when the table of contents, list of figures, or list of
tables needs a forced rebuild.

The reference ABI is generated separately from `spec/abi.yaml`:

```sh
make -C isa abi-pdf
make -C isa abi-pdf-final
```

Validation runs before generation so generated artifacts are never emitted from
an internally inconsistent spec.

## Pattern DSL

Patterns are written most-significant-bit first.

- `0` and `1` are fixed bits.
- `-`, `?`, and `.` are wildcards.
- alphabetic symbols are variable fields.
- whitespace, `_`, and `|` are ignored.

Fields may be declared beside an instruction or EA form to make width
validation explicit. Repeated single-letter fields such as `ddd` are counted as
one 3-bit field. Multi-character declared fields, such as `zz`, are matched as a
single symbolic field when present in the declaration.
