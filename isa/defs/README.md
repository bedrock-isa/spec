# Instruction Definitions

`isa/defs` contains semantic instruction definitions for the current ISA.
Concrete opcode placement is intentionally externalized to `isa/alloc`.

The current contents are a first-pass import from `old/isa/spec`:

```text
old allocation blocks removed
instruction families and extension families preserved
old operand schema migrated to extension-aware operand files
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

Extension-wide machine-readable invariants live in the extension root's
`extension.yaml`. The top-level `extensions.yaml` lists root extension names,
and each extension references its sub-extensions explicitly. Instruction-set
`instructions.yaml` files are indexes only; they do not provide ambient
defaults or implicit inheritance for individual instruction definitions. The
loader qualifies child extension names by ancestry, such as
`fpu.transcendental_approx`.

Architectural register declarations use named groups with a common `entries`
shape. Base groups live in the top-level `registers.yaml`; extension-owned
groups live in that extension's `registers.yaml` and are referenced by its
`extension.yaml`. Addressing-mode encodings and fixed segment selection remain
owned by `ea.yaml`, not by register declarations. EA payload widths, compact
forms, and EXT0 descriptor forms are declared there once; the corresponding
LaTeX encoding and syntax lists are generated from those declarations.

Base instructions and their index live directly under `isa/defs`. Base operand
types live in the top-level `operands.yaml`; extension-owned operand types live
in that extension's `operands.yaml` and are referenced by its `extension.yaml`.
Each operand type owns its encoding kind, field width, and any
type-specific values or immediate rules. Instruction-size codes and field
encodings are kept separately in `sizes.yaml`; extension-owned sizes use the
same arrangement.

Approximate floating-point instructions additionally own a structured
`behavior.approximation` block. Its stable contract ID, reference function,
domain, ISA ULP ceiling, exact anchors, and mathematical properties are the
source of truth for both the instruction page and CPUID accuracy-contract
tables. Do not duplicate that mapping in a documentation template.

Run the definition-layer check with:

```sh
python3 isa/tools/validate_defs.py
```
