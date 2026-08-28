# Bedrock

Bedrock is a 64-bit instruction set architecture and systems-software specification. The specification covers the programmer-visible architecture, a 64-bit ELF environment, and an LP64 C ABI.

## A Bedrock instruction in one glance

```asm
REP R1, ADD.Q [DS:R2 + R3++ * 8 + 32], R4
```

Repeat the scalar `ADD.Q` body `R1` times: add the 64-bit value at `DS:(R2 + R3 * 8 + 32)` to `R4`, increment the element index `R3` after every committed iteration, and retain a precise restart boundary if an iteration faults.

For an overview of the architecture, read the [Architectural Introduction](docs/introduction.md).

## LLVM and samples

The default workspace layout places `spec` and `llvm-project` next to each
other, with LLVM configured in `llvm-project/build`. Override
`LLVM_PROJECT_ROOT`, `LLVM_BUILD_DIR`, or `LLVM_BIN` for another layout.

```sh
python3 -m pip install -r requirements.txt
make llvm             # synchronize generated inputs and build Bedrock LLVM tools
make samples-check    # build samples and validate their ELF outputs
make tiny-kernel      # build samples/tiny_kernel/build/tiny_kernel.elf
```

The tiny-kernel emulator acceptance test uses the same Python interpreter for
catalog generation:

```sh
PYTHON=/path/to/python \
BEDROCK_LLVM_ROOT=../llvm-project/build \
make -C samples/tiny_kernel test
```

## Testing

Run `make test-pr` for the canonical local PR gate. It validates the ISA
definitions and conformance manifest, runs every non-SystemVerilog ISA Python
owner suite including the Sail generation checks, checks emulator ISA
generation and Rust formatting, tests the Rust workspace except `bedrock-lldb`
and `bedrock-gui`, and runs the SystemVerilog decoder owner suite. When
Verilator is installed, that suite also performs its bounded package and D0
checks.

The PR gate does not run the external LLVM/LLDB-dependent workspace crates. In
an environment configured with the Bedrock LLVM/LLDB build, run
`make emulator-validate` for the complete emulator workspace lane. See the
[Sail executable architecture model](isa/README.md) for Sail model typechecking
and detailed model/test commands.

## License

This project is licensed under the [Apache License 2.0](LICENSE).
