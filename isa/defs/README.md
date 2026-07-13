# Instruction Definitions

`isa/defs` contains semantic instruction definitions for the current ISA.
Concrete opcode placement is intentionally externalized to `isa/alloc`.

The current contents are a first-pass import from `old/isa/spec`:

```text
old allocation blocks removed
instruction families and extension families preserved
old extension family ordering preserved in manifest.yaml, except removed legacy core groups
old operand schema preserved in operands.yaml
```

This import is being migrated to the new architectural model. Base instruction
operand types use `Rn`; removed legacy core instructions are not kept as
inactive definitions in this tree.

Definition YAML is reserved for encodings, enumerated values, operand forms,
and constraints owned by a concrete instruction or format. Cross-cutting
explanatory prose belongs in the reference templates, not in generic
`rule`/`meaning`, `topic`/`value`, or similar document-shaped mappings. A
derived list must be computed from its owning definitions instead of being
copied into a second YAML source. The `doc` block on an instruction remains the
intentional home for that instruction's title, summary, and narrative.

Approximate floating-point instructions additionally own a structured
`behavior.approximation` block. Its stable contract ID, reference function,
domain, ISA ULP ceiling, exact anchors, and mathematical properties are the
source of truth for both the instruction page and CPUID accuracy-contract
tables. Do not duplicate that mapping in a documentation template.

Run the definition-layer check with:

```sh
python3 isa/tools/validate_defs.py
```
