# Sail executable architecture model

Authority is divided by domain. `isa/instructions/definitions` owns instruction
encodings, operand grammar, stable form identities, extension wiring, and
document order; `isa/addressing/effective_address/definition.yaml` owns the
effective-address grammar. The handwritten Sail files colocated under the
semantic topic directories in `isa` own executable instruction behavior, architectural state
transitions, fault and commit ordering, repeat and event behavior, and the
sequence of memory actions issued by one hart. The formal memory model owns
permitted cross-hart ordering and visibility. ABI sources own ELF, C ABI, and
calling-convention contracts;
compiler-interface sources separately own source-language and compiler-facing
target-interface contracts.

In the handwritten Sail and formal-model internals, one hart corresponds to one architectural logical processor.
Public ISA prose uses *logical processor*; the internal hart and memory-action terms do not define additional
architectural subjects or public memory-event categories.

Numerical floating-point primitives, including FPTRANSA reference values and
ULP certificates, are trusted external inputs. The Sail model owns validation
of their contract identity and shape, reported error bound, NX exclusion, and
architectural commit or trap behavior; it does not independently recompute the
provider's numerical result.

Handwritten explanatory prose is an authored, semantically downstream view of
the owner for its domain. Behavioral prose must be traceable to this Sail model
and cannot independently introduce observable behavior. Encoding, concurrency,
and ABI prose are similarly downstream of their respective owners.

The layout follows semantic ISA topics rather than source representation:

```text
isa/
├── bedrock.sail_project      handwritten module graph
├── addressing/
│   └── effective_address/    definition, decode, evaluation, and manual roles
├── conformance/              shared conformance manifest and data
├── encoding/
│   ├── data/                 explanatory TeX
│   └── instruction/          explanatory TeX + Sail decode/catalog types
├── execution/
│   ├── core/                 explanatory TeX + Sail execution boundary
│   └── repeat/               explanatory TeX + Sail repeat behavior
├── foundations/
│   └── architecture/         explanatory TeX + Sail foundations
├── instructions/
│   ├── definitions/          instruction YAML, schema, and extension wiring
│   ├── manual/               shared instruction-reference TeX
│   └── semantics/            integer, control, and floating-point Sail
├── interfaces/
│   ├── abi/                  ELF/C ABI sources and conformance inputs
│   └── c/                    compiler-facing intrinsics and headers
├── manual/
│   ├── common/               shared TeX definitions
│   └── document/             manual assembly and front matter
├── memory/
│   ├── access/               memory accesses and continuation
│   ├── cache/                cache-operation model
│   ├── ordering/             manual and formal ordering model
│   └── translation/          model, manual, and conformance roles
├── system/
│   ├── events/               explanatory TeX + Sail event behavior
│   ├── requests/             system-request processing
│   ├── stack/                stack-memory operations
│   ├── state/                explanatory TeX + Sail system state
│   └── indexes/              explanatory TeX navigation
├── tests/                    semantic-family tests and executable entrypoint
└── tools/                    generators, validators, and Sail tooling
```

Per-instruction prose is generated from `isa/instructions/definitions`; the
semantic leaves therefore do not contain authored TeX counterparts.

The source project contains handwritten Sail only. The generator writes the
operations, catalog, and `bedrock-generated.sail_project` overlay into an
explicit build directory; Sail composes that overlay with the handwritten
project. Generated Sail is a build artifact and is never an authority owner.
Only `foundations/architecture/prelude.sail` uses Sail library `$include`
directives.

The canonical Decode IR also generates four disposable combinational
SystemVerilog artifacts: `bedrock_decode_pkg.sv`, `bedrock_decode_d0.sv`,
`bedrock_decode_d1.sv`, and `bedrock_decode_ea.sv`. D0 accepts a valid bit,
generated opcode-class enum, and right-aligned 34-bit opcode, and returns a
recognition result in one of four states: invalid input, unallocated opcode,
constraint-rejected, or success. A successful result also carries the selected
form's two-bit EA layout and the operand width for each of two fixed EA
candidates. In parallel, D0 emits a separate packed EA-front-end result carrying
the same status/layout/widths plus the low/alternate compact fields and the
base/post-alternate record cursors. The opcode D1 consumes the recognition
result, while the EA D1 consumes the EA-front-end result; each also accepts an
18-byte record with byte 0 in bits `[7:0]` and a byte count.
`bedrock_decode_d1` emits the packed opcode/form result: valid/stage,
form and operation, control metadata, size/flag/event masks, four compact
operands with fixed low/alternate EA-candidate references, overlap, and
required/encoded byte counts. `bedrock_decode_ea` speculatively decodes exactly
two class-position candidates: medium low plus medium-alt, or long/extralong
low plus high. Unreferenced candidates are ignored; D0 precomputes both record
cursors, and only a high-then-low layout selects the post-alternate cursor for
the low candidate. It emits an independent packed EA result containing its
own valid/stage, the two fixed canonical candidates, and required-byte evidence.
Neither module consumes the other's result and no aggregate packet or join
module is generated;
downstream control combines only their success/kill conditions for referenced
EA candidates. Richer Decode IR metadata remains outside both buses. The
interfaces use `logic` enums and packed structures and have no clock, reset,
register, or transport protocol.

For source-only reading, begin with `isa/bedrock.sail_project`, which is the
ordered module graph. `foundations/architecture/` defines shared semantic types;
the generated overlay supplies operation and encoding metadata from
`isa/instructions/definitions`; `encoding/instruction/` and
`addressing/effective_address/decode/` turn records into decoded instructions;
the execution, memory, system, and instruction leaves contain their applicable state, behavior,
and numerical-provider sources; and `execution/core/boundary.sail` defines
architectural execution boundaries.

The larger handwritten sources are divided by responsibility within those same
semantic leaves. In project order:

- `encoding/instruction/` contains `selected.sail`, `types.sail`, `bytes.sail`,
  and `decode.sail` for the selected subset, decoded types, byte extraction,
  and full-record decode. Effective-address parsing is in
  `addressing/effective_address/decode/effective_address.sail`.
- `instructions/semantics/floating_point/` contains `operation_catalog.sail`,
  `transcendental_contract.sail`, and `register_pairs.sail` for catalog metadata;
  `environment.sail`, `local_operations.sail`, `request_contract.sail`,
  `response_contract.sail`, and `finalize.sail` for provider semantics; and
  `local_execution.sail`, `transaction_inputs.sail`,
  `transaction_compute.sail`, and `transaction_flow.sail` for execution.
- `execution/core/` contains `state.sail`, `predicates.sail`, and
  `integer_bits.sail` for shared execution support. Effective-address evaluation
  is in `addressing/effective_address/evaluation/`.
  Resume support is in `resume_values.sail`, `resume_restore.sail`, and
  `resume_common.sail`; the memory phase is in `memory/access/continuation.sail`,
  while the other phase implementations are in `resume_control.sail`,
  `resume_system.sail`, `resume_repeat.sail`,
  `resume_events.sail`, and `resume_fp.sail`; `resume.sail` owns response
  validation and phase dispatch.
- `instructions/semantics/integer/` contains `operands.sail`, `arithmetic.sail`,
  `data_control.sail`, and `routing.sail`. Memory access, cache, translation,
  and ordering sources use the corresponding role directories under `memory/`;
  system reset, save/restore, requests, and stack operations are under
  `system/`.
- `tests/` keeps aggregate test entrypoints in `protocol.sail`, `event.sail`, and
  `floating_point.sail`; their responsibility-group helpers use the matching
  `protocol_*`, `event_support.sail`, and `floating_point_*` filenames.

These are source-navigation divisions only. They do not create additional
semantic leaves or authored TeX counterparts.

Build the consumer documentation artifact from the repository root:

```sh
make sail-docs
```

This writes only beneath the ignored `build/sail-doc/` directory. Its primary
outputs are Sail's embedded documentation bundle, `bedrock-sail.json`, and the
deterministic `semantic-index.json`. The index maps each generated operation to
its route, each stable form ID to its operation, and module-qualified actual
owner paths derived from the `core`, `fp`, and `postlude` functions and their
dispatch. Operations without an operation-specific owner are accepted only
when their route has an explicit owner.

From the repository root:

```sh
isa_sail_build=$(mktemp -d /private/tmp/isa-sail.XXXXXX)
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/sail/generate_catalog.py \
  "$isa_sail_build"
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/sail/generate_catalog.py \
  "$isa_sail_build" --check
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/sail/test_generation.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=isa/tools python3 isa/tools/validate_isa.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=isa/tools python3 isa/tools/validate_alloc.py
(cd isa && opam exec -- sail --require-version 0.20.2 --no-memo-z3 \
  --all-modules --just-check bedrock.sail_project \
  "$isa_sail_build/bedrock-generated.sail_project")
```

Generate, check, test, and validate the SystemVerilog decoder from the
repository root:

```sh
sv_build=$(mktemp -d /private/tmp/isa-sv-decoder.XXXXXX)
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/systemverilog/generate_decoder.py \
  "$sv_build"
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/systemverilog/generate_decoder.py \
  "$sv_build" --check
PYTHONDONTWRITEBYTECODE=1 SV_TEST_ROOT="$sv_build/tests" \
  python3 isa/tools/systemverilog/test_generation.py
make sv-decoder SV_BUILD_DIR="$sv_build/make"
```

The owner suite performs bounded package/D0 Verilator checks when Verilator is
available. Full lint of both large split-D1 modules is intentionally opt-in via
`SV_RUN_LARGE_LINT=1` because elaboration can require several gigabytes of
memory.

Generate and run C only in a temporary directory:

```sh
isa_sail_build=$(mktemp -d /private/tmp/isa-sail.XXXXXX)
PYTHONDONTWRITEBYTECODE=1 python3 isa/tools/sail/generate_catalog.py \
  "$isa_sail_build"
gmp_prefix=$(brew --prefix gmp)
(cd isa && C_INCLUDE_PATH="$gmp_prefix/include" LIBRARY_PATH="$gmp_prefix/lib" \
  opam exec -- sail --require-version 0.20.2 --no-memo-z3 --all-modules \
  -c --c-build -o "$isa_sail_build/bedrock_tests" bedrock.sail_project \
  "$isa_sail_build/bedrock-generated.sail_project")
"$isa_sail_build/bedrock_tests"
```
