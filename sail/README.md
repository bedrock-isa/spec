# Sail executable architecture model

Authority is divided by domain. `isa/defs` owns instruction encodings, operand
and effective-address grammar, stable form identities, extension wiring, and
document order. The handwritten files under `sail/model` own executable
instruction behavior, architectural state transitions, fault and commit
ordering, repeat and event behavior, and the sequence of memory actions issued
by one hart. The formal memory model owns permitted cross-hart ordering and
visibility. ABI sources own ELF, C ABI, and calling-convention contracts;
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

The layout follows a Sail project rather than textual source aggregation:

```text
sail/
├── tools/                 deterministic catalog generator and freshness tests
└── model/
    ├── bedrock.sail_project  handwritten module graph
    ├── prelude/ catalog/ decode/ fp/
    ├── core/ postlude/       execution state machine and boundary API
    ├── unit_tests/           semantic-family tests
    └── main/                 executable smoke and full-test entrypoint
```

The source project contains handwritten Sail only. The generator writes the
operations, catalog, and `bedrock-generated.sail_project` overlay into an
explicit build directory; Sail composes that overlay with the handwritten
project. Generated Sail is a build artifact and is never an authority owner.
Only `prelude/prelude.sail` uses Sail library `$include` directives.

For source-only reading, begin with `model/bedrock.sail_project`, which is the
ordered module graph. `prelude/` defines shared semantic types; the generated
overlay supplies operation and encoding metadata from `isa/defs`; `decode/`
turns records into decoded instructions; `core/` defines state, execution,
fault, transaction, repeat, and event behavior; `fp/` defines the numerical
provider boundary; and `postlude/` defines architectural execution boundaries.

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
PYTHONDONTWRITEBYTECODE=1 python3 sail/tools/generate_catalog.py \
  "$isa_sail_build"
PYTHONDONTWRITEBYTECODE=1 python3 sail/tools/generate_catalog.py \
  "$isa_sail_build" --check
PYTHONDONTWRITEBYTECODE=1 python3 sail/tools/test_generation.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=isa/tools python3 isa/tools/validate_isa.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=isa/tools python3 isa/tools/validate_alloc.py
(cd sail/model && opam exec -- sail --require-version 0.20.2 --no-memo-z3 \
  --all-modules --just-check bedrock.sail_project \
  "$isa_sail_build/bedrock-generated.sail_project")
```

Generate and run C only in a temporary directory:

```sh
isa_sail_build=$(mktemp -d /private/tmp/isa-sail.XXXXXX)
PYTHONDONTWRITEBYTECODE=1 python3 sail/tools/generate_catalog.py \
  "$isa_sail_build"
gmp_prefix=$(brew --prefix gmp)
(cd sail/model && C_INCLUDE_PATH="$gmp_prefix/include" LIBRARY_PATH="$gmp_prefix/lib" \
  opam exec -- sail --require-version 0.20.2 --no-memo-z3 --all-modules \
  -c --c-build -o "$isa_sail_build/bedrock_tests" bedrock.sail_project \
  "$isa_sail_build/bedrock-generated.sail_project")
"$isa_sail_build/bedrock_tests"
```
