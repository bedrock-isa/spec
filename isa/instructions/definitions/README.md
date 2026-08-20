# Instruction Definitions

`isa/instructions/definitions` is the source of truth for concrete instruction
encodings, operand grammar, stable form identities, extension wiring,
structured static facts, and document order. Effective-address grammar is
owned by `isa/addressing/effective_address/definition.yaml`. Handwritten Sail owns executable
instruction behavior, architectural state transitions, fault and commit
ordering, repeat and event behavior, and single-hart memory-action sequencing.
The formal memory model owns its concurrency domain. ABI sources own ELF, C
ABI, and calling-convention contracts, while compiler-interface sources
separately own source-language and compiler-facing target-interface contracts.

Encoding forms are instruction-owned. Instruction and extension families are
explicit, and base instruction operand types use `Rn`.

Definition YAML is reserved for stable, structured values. Cross-cutting
explanatory prose belongs in the reference templates, not in generic
`rule`/`meaning`, `topic`/`value`, or similar document-shaped mappings. A
derived list must be computed from its owning definitions instead of being
copied into a second YAML source.

The exact versioned contract is documented in `SCHEMA.md`. The dataclass
decoder and `schema.lock` reject unknown fields, wrong scalar types,
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

Instruction attributes contain class, family, and privilege. Where applicable,
the sibling `repeat` record contains accepted repeat contexts. FLAGS and FFLAGS effects are structured instruction
metadata so reference tables and compact effect lines are generated from one
source. Handwritten explanatory text remains authored prose, but descriptions
of executable behavior must be traceable to the applicable handwritten Sail
functions and cannot independently introduce an observable state transition,
fault, commit, repeat, event, or memory action. Encoding prose remains
downstream of these definitions.

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
owned by `isa/addressing/effective_address/definition.yaml`, not by register
declarations. EA payload widths, compact forms, and exact-length EXT1 and EXT2
descriptor forms are declared there
once; the corresponding LaTeX encoding and syntax lists are generated from
those declarations.

Base instructions and their index live directly under
`isa/instructions/definitions`. Base operand types live in the top-level
`operands.yaml`; extension-owned operand types live
in that extension's `operands.yaml` and are referenced by its `extension.yaml`.
Each operand type owns its encoding kind, field width, and any
type-specific values or immediate rules. Instruction-size codes and field
encodings are kept separately in `sizes.yaml`; extension-owned sizes use the
same arrangement.

The transcendental-approximation extension manifest contains only extension
wiring and its feature association. The external numerical provider owns
reference values and ULP certificates; handwritten Sail owns validation and
architectural trap or commit behavior. The authored presentation remains in
the extension's `introduction.tex`, sibling `details.tex` files, and
`fptransa_accuracy_contracts.tex`, downstream of those owners and without
duplication as instruction or extension YAML metadata.

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
