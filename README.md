# ISA Design Rewrite

This repository is being rewritten around hand-authored ISA allocation tables.
The previous implementation, generated artifacts, and reference material live
under `old/`.

Current active sources:

```text
docs/isa_reform_plan.md      design notes and current architectural direction
isa/defs/*.yaml              instruction semantics and architectural definitions
isa/alloc/*.yaml             opcode allocation source of truth
isa/tools/validate_defs.py   definition include/family consistency validator
isa/tools/validate_alloc.py  allocation collision and cardinality validator
isa/tools/validate_isa.py    definition/allocation join validator
isa/tools/gen_docs.py        draft reference document generator
```

Run the current checks with:

```sh
python3 isa/tools/validate_defs.py
python3 isa/tools/validate_alloc.py
python3 isa/tools/validate_isa.py
```

Generate the draft reference document with:

```sh
python3 isa/tools/gen_docs.py -o build/isa_reference.md
```

The generator can also emit a preview TeX file:

```sh
python3 isa/tools/gen_docs.py --format latex -o build/isa_reference.tex
```
