# Bedrock Emulator

This directory contains a Rust workspace for a Bedrock CPU emulator. It
includes the Sail core bridge, memory bus, memory-mapped
framebuffer/keyboard devices, concrete machine wiring, debugger support, CLI,
GUI, LLVM toolchain integration, and executable samples.

The emulator is a non-owning executable consumer of the surrounding ISA
repository. Handwritten Sail under `../sail` owns executable architectural
behavior. `../artifacts/emulator-core` generates the stable C ABI consumed by
the Rust `bedrock-sail-core` bridge; the emulator has no independent Rust ISA
decoder or execution core.

## Workspace Layout

- `bedrock-bus`: byte-addressed bus, RAM, devices, and address-map helpers.
- `bedrock-sail-core`: Rust bridge to the generated Sail emulator core.
- `bedrock-devices`: framebuffer and keyboard MMIO devices.
- `bedrock-machine`: concrete MVP board wiring and frontend architecture types.
- `bedrock-debug`: breakpoint, watchpoint, trace, and snapshot types.
- `bedrock-toolchain`: LLVM Bedrock toolchain process wrapper.
- `bedrock-cli`: headless ELF runner and GDB remote server entrypoint.
- `bedrock-gui`: egui debugger with CPU, display, memory, disassembly,
  keyboard, and trace panels.

## Checks

From the ISA repository root, validate the complete emulator:

```sh
make emulator-validate
```

Sail artifact generation requires Python 3 and PyYAML. The Sail bridge invokes
the artifact generator when its declared inputs change; set `PYTHON` to
override the default `python3` executable. From this directory, the equivalent
direct Cargo checks are:

```sh
cargo check --workspace
cargo test --workspace
```

## Loading ELF Images

The headless runner can load a Bedrock ELF64 executable and reset the CPU to
the ELF entry point in privileged `STATUS.PM` boot state:

```sh
cargo run -p bedrock-cli -- --elf path/to/program.elf --steps 1
```

For `ET_DYN` executables, pass a load bias:

```sh
cargo run -p bedrock-cli -- --elf path/to/program.elf --load-base 0x4000
```

Numeric CLI parameters accept decimal or `0x` hexadecimal values, and `_`
separators are allowed.

## GUI

Run the native debugger UI with:

```sh
cargo run -p bedrock-gui
```

The GUI can load ELF images, run or single-step the machine, edit software
breakpoints, display the RGB332 framebuffer, inspect RAM, inject keyboard
events, and show LLVM `objdump` output for the loaded ELF.

## Samples

`../samples/tiny_kernel` builds a small kernel with a TTY shell. Shell commands
such as `MATH`, `SORT`, `MEM`, `DEMO`, `FAULT`, `HALT`, and `BASIC` load
separate embedded ELF user applications into their own code/data and stack
address ranges, switch to user mode, and then return to the shell through
`SYSCALL_EXIT` when appropriate. `BASIC` starts a BASIC-like prompt with `LIST`,
`RUN`, `PRINT`, `HELP`, and `EXIT`; `RUN` executes a small VM that uses
compiler-emitted double-precision FPU instructions (`FMOV.D`, `FADD.D`,
`FMUL.D`, `FDIV.D`, and `FSUB.D`).

## LLVM Toolchain

Assembler and disassembler work must go through the external Bedrock LLVM
toolchain via `bedrock-toolchain`; the emulator should not duplicate assembly
syntax or disassembly formatting in Rust. Full `cargo test --workspace` and
`make emulator-validate` runs include the LLDB crate, so they require a
complete LLVM checkout and build, including its headers and libraries.

The LLVM toolchain discovery uses the following order:
1. `BEDROCK_LLVM_BIN`, when set, names the LLVM tool binary directory.
2. Otherwise, `BEDROCK_LLVM_ROOT/bin` is used.

Set the LLVM build directory for full-workspace builds, which need its headers
and libraries as well as its tools. The LLDB source headers are taken from the
sibling checkout path `BEDROCK_LLVM_ROOT/../lldb/include`:

```sh
export BEDROCK_LLVM_ROOT=/absolute/path/to/llvm/build
```

To override only executable lookup, set the binary directory explicitly:

```sh
export BEDROCK_LLVM_BIN=/absolute/path/to/llvm/build/bin
```

If neither variable is set, toolchain discovery returns a missing-configuration
error. `BEDROCK_LLVM_BIN` does not provide the build root needed for LLDB
headers and LLVM libraries; those paths always derive from
`BEDROCK_LLVM_ROOT`. The toolchain wrapper runs:

```sh
llvm-mc -triple=bedrock-unknown-unknown -filetype=obj program.s -o program.o
ld.lld -m elf64bedrock program.o --image-base=0 -Ttext=0x1000 -o program.elf
llvm-objdump -d --no-show-raw-insn program.elf
```
