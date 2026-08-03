# Instruction Definitions

`isa/defs` is the source of truth for instruction documentation, concrete
encodings, architectural primitives, extension wiring, and document order.

Encoding forms are instruction-owned. Instruction and extension families are
explicit, and base instruction operand types use `Rn`.

Definition YAML is reserved for stable, structured values. Cross-cutting
explanatory prose belongs in the reference templates, not in generic
`rule`/`meaning`, `topic`/`value`, or similar document-shaped mappings. A
derived list must be computed from its owning definitions instead of being
copied into a second YAML source.

The exact versioned contract is documented in `SCHEMA.md`. The frozen
dataclass decoder and `schema.lock` reject unknown fields, wrong scalar types,
invalid discriminated variants, and unversioned changes to the decoder itself.

Each instruction directory contains two required YAML documents:

```text
instruction.yaml  title, summary, description, attributes, flag effects, and optional TeX/syntax references
encodings.yaml    concrete forms with stable ID, class, bits, syntax, operands, sizes, fields, and constraints
```

Every encoded operand has a `name`, registered operand `type`, and one of the
common `access` values `read`, `write`, `read_write`, or `address`. It names its
opcode marker with `field` unless it is a fixed or payload-only operand. A
user-domain memory operand additionally carries `domain: user`; the ordinary
current domain is implicit. `fields` declares non-operand selectors such as a
size field. Field widths are derived from `bits` rather than repeated.

Instruction attributes contain class, family, privilege, and, where applicable,
accepted repeat contexts. Flag semantics and other instruction-specific
normative detail live in the explicitly referenced TeX body. FLAGS and FFLAGS
effects are structured instruction metadata so reference tables and compact
effect lines are generated from one source. Implicit state
reads and writes are described there rather than duplicated in unconsumed YAML.

The five encoding classes and their order are architectural invariants in
`isa/tools/encoding_architecture.py`. Payload widths and opcode namespaces are
derived there from instruction framing and the extended opcode selectors.
Allocation validation, reports, documentation, and `alloc_edit.py` aggregate
the per-instruction `encodings.yaml` files against that fixed grammar.

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

The transcendental-approximation extension manifest contains only extension
wiring and its feature association. The common approximation model and
individual instruction contracts are normative TeX: the common model lives in
the extension's `introduction.tex`, instruction-specific semantics live in
sibling `details.tex` files, and the CPUID registry lives in
`fptransa_accuracy_contracts.tex`. This documentation is not duplicated as
instruction or extension YAML metadata.

The document compiler owns the definition-layer checks and the full document
gate:

```sh
make docs
```

Generate allocation reports with `python3 isa/tools/gen_alloc_report.py`.
Inspect the global space with `alloc_edit.py summary`, `entries`, `check`, or
`holes`. The write commands operate on stable form IDs:

```sh
python3 isa/tools/alloc_edit.py add MNEMONIC form.yaml
python3 isa/tools/alloc_edit.py move FORM_ID --class long --bits '...'
python3 isa/tools/alloc_edit.py edit FORM_ID --bits '...' --constraints constraints.yaml
```

Write commands print a unified diff and make no change by default. `--apply`
strictly decodes the candidate, checks registered references and the complete
global opcode space, then atomically replaces the one `encodings.yaml` file.
