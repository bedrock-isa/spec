# Sail executable architecture model

Authority is divided by domain. `isa/defs` owns instruction encodings, operand
and effective-address grammar, stable form identities, extension wiring, and
document order. The handwritten Sail files colocated under the semantic topic
directories in `isa` own executable instruction behavior, architectural state
transitions, fault and commit ordering, repeat and event behavior, and the
sequence of memory actions issued by one hart. The formal memory model owns
permitted cross-hart ordering and visibility. ABI sources own ELF, C ABI, and
calling-convention contracts;
compiler-interface sources separately own source-language and compiler-facing
target-interface contracts.

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
├── document/                 manual assembly and front matter
├── foundations/
│   └── architecture/         explanatory TeX + Sail foundations
├── encoding/
│   ├── data/                 explanatory TeX
│   └── instruction/          explanatory TeX + Sail decode/catalog types
├── addressing/
│   └── effective_address/    explanatory TeX
├── execution/
│   ├── core/                 explanatory TeX + Sail execution boundary
│   └── repeat/               explanatory TeX + Sail repeat behavior
├── memory/
│   └── architecture/         explanatory TeX + Sail memory behavior
├── system/
│   ├── events/               explanatory TeX + Sail event behavior
│   ├── state/                explanatory TeX + Sail system state
│   └── indexes/              explanatory TeX navigation
├── instructions/
│   ├── integer/              Sail execution semantics
│   ├── control/              Sail execution semantics
│   ├── floating_point/       Sail execution and provider semantics
│   └── reference/            shared explanatory TeX
├── tests/                    semantic-family tests and executable entrypoint
└── tools/sail/               deterministic catalog generator and freshness tests
```

Per-instruction prose is generated from `isa/defs`; the `integer/`, `control/`,
and `floating_point/` leaves therefore do not contain authored TeX counterparts.

The source project contains handwritten Sail only. The generator writes the
operations, catalog, and `bedrock-generated.sail_project` overlay into an
explicit build directory; Sail composes that overlay with the handwritten
project. Generated Sail is a build artifact and is never an authority owner.
Only `foundations/architecture/prelude.sail` uses Sail library `$include`
directives.

For source-only reading, begin with `isa/bedrock.sail_project`, which is the
ordered module graph. `foundations/architecture/` defines shared semantic types;
the generated overlay supplies operation and encoding metadata from `isa/defs`;
`encoding/instruction/` turns records into decoded instructions; the execution,
memory, system, and instruction leaves contain their applicable state, behavior,
and numerical-provider sources; and `execution/core/boundary.sail` defines
architectural execution boundaries.

The larger handwritten sources are divided by responsibility within those same
semantic leaves. In project order:

- `encoding/instruction/` contains `selected.sail`, `types.sail`, `bytes.sail`,
  `effective_address.sail`, and `decode.sail` for the selected subset, decoded
  types, byte extraction, effective-address parsing, and full-record decode.
- `instructions/floating_point/` contains `operation_catalog.sail`,
  `transcendental_contract.sail`, and `register_pairs.sail` for catalog metadata;
  `environment.sail`, `local_operations.sail`, `request_contract.sail`,
  `response_contract.sail`, and `finalize.sail` for provider semantics; and
  `local_execution.sail`, `transaction_inputs.sail`,
  `transaction_compute.sail`, and `transaction_flow.sail` for execution.
- `execution/core/` contains `state.sail`, `predicates.sail`,
  `effective_address.sail`, and `integer_bits.sail` for shared execution support.
  Resume support is in `resume_values.sail`, `resume_restore.sail`, and
  `resume_common.sail`; phase implementations are in `resume_memory.sail`,
  `resume_control.sail`, `resume_system.sail`, `resume_repeat.sail`,
  `resume_events.sail`, and `resume_fp.sail`; `resume.sail` owns response
  validation and phase dispatch.
- `instructions/integer/` contains `operands.sail`, `arithmetic.sail`,
  `data_control.sail`, and `routing.sail`. `memory/architecture/` contains
  `common.sail`, `save_cache.sail`, `translation.sail`,
  `system_requests.sail`, and `stack_control.sail`.
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
deterministic `semantic-index.json`. The index maps all 205 operations to their
routes, all 422 stable form IDs to their operations, and module-qualified actual
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
