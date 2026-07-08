# Instruction Definitions

`isa/defs` contains semantic instruction definitions for the ISA rewrite.
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

Run the definition-layer check with:

```sh
python3 isa/tools/validate_defs.py
```
