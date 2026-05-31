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
- `tools/gen_sleigh.py`: emits a starter SLEIGH file.
- `tools/alloc_z3.py`: validates allocator inputs, checks semantic/spec
  alignment, generates operand-field layouts from semantic operands, and uses
  Z3 to choose between one-word primary encodings and generated extended-opcode
  descriptor forms. It generates natural primary extension roots from semantic
  families and operand layouts, while preserving primary headroom for later
  growth. Sentinel payloads remain explicit; instruction opcode placements do
  not.
- `../build/generated/`: generated artifacts derived from `spec/`.
- `tests/`: reserved for decode, encode, canonicalization, and overlap regression cases.

## Common Commands

Run these from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/validate.py isa/spec
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/alloc_z3.py isa/spec -o build/generated/allocation_plan.json --md-output build/generated/opcode_table.md
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/gen_instruction_tables.py isa/spec --allocation build/generated/allocation_plan.json -o build/generated/instruction_encoding_table.md
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/gen_instruction_specs.py isa/spec --allocation build/generated/allocation_plan.json -o build/generated/instruction_specs.md
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/gen_tables.py isa/spec --allocation build/generated/allocation_plan.json -o build/generated/opcode_map.md
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/decodegen.py isa/spec --allocation build/generated/allocation_plan.json -o build/generated/decoder_table.json
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/encodegen.py isa/spec --allocation build/generated/allocation_plan.json -o build/generated/encoder_table.json
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/gen_sleigh.py isa/spec --allocation build/generated/allocation_plan.json -o build/generated/isa.slaspec
```

The LaTeX manual can be built from the repository root:

```sh
make manual-pdf
make manual-pdf PDF_PASSES=2
make manual-pdf-final
```

`manual-pdf` defaults to one `pdflatex` pass for quick iteration. Use
`PDF_PASSES=2` or `manual-pdf-final` when the table of contents, list of
figures, or list of tables needs a second pass.

The reference ABI is generated separately from `spec/abi.yaml`:

```sh
make abi-pdf
make abi-pdf PDF_PASSES=2
make abi-pdf-final
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
