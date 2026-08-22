# Bedrock Emulator

This directory contains a Rust workspace for a Bedrock CPU emulator. It
includes the CPU core, ISA decoder, memory bus, memory-mapped
framebuffer/keyboard devices, concrete machine wiring, debugger support, CLI,
GUI, LLVM toolchain integration, and executable samples.

The emulator is a non-owning executable consumer of the surrounding ISA
repository. Static instruction definitions come from
`../isa/instructions/definitions`, and EA grammar comes from
`../isa/addressing/effective_address/definition.yaml`;
handwritten Sail under `../sail` owns executable architectural behavior. The
Rust decode table is generated into Cargo's build output from the definitions
and does not independently define the ISA. No generated Rust source is checked
into a crate `src` directory.

## Workspace Layout

- `bedrock-isa`: instruction word, prefix, operand, and decode skeletons.
- `bedrock-bus`: byte-addressed bus, RAM, devices, and address-map helpers.
- `bedrock-core`: CPU state, memory translation, exception delivery, integer
  execution, and the executable FPU subset used by the samples.
- `bedrock-devices`: framebuffer and keyboard MMIO devices.
- `bedrock-machine`: concrete MVP board wiring.
- `bedrock-debug`: breakpoint, watchpoint, trace, and snapshot types.
- `bedrock-toolchain`: LLVM Bedrock toolchain process wrapper.
- `bedrock-cli`: headless ELF runner and GDB remote server entrypoint.
- `bedrock-gui`: egui debugger with CPU, display, memory, disassembly,
  keyboard, and trace panels.

## Checks

From the ISA repository root, check the generator and the complete emulator:

```sh
make emulator-isa-check
make emulator-validate
```

Generation requires Python 3 and PyYAML. Cargo invokes the generator
automatically for direct builds, checks, and tests; set `PYTHON` to override
the default `python3` executable. From this directory, the equivalent direct
Cargo checks are:

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
