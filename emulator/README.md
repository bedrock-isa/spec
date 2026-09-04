# Bedrock Emulator

The emulator executes the architecture owned by the surrounding ISA sources.
The `artifacts/emulator-core` generator projects those sources through an
internal C interface consumed by the Rust `bedrock-sail-core` crate.

Validate the generated core and Rust workspace from the specification root:

```sh
make emulator-validate
```

LLVM-dependent crates require `BEDROCK_LLVM_ROOT` to name an LLVM build tree
containing its headers and libraries. `BEDROCK_LLVM_BIN` may name a separate
directory containing the LLVM executables.
