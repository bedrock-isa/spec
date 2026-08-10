# Bedrock Emulator

This directory contains an early Rust workspace for a Bedrock CPU emulator.
It now includes the CPU core, ISA decoder, memory bus, memory-mapped
framebuffer/keyboard devices, concrete machine wiring, debugger support, CLI,
GUI, LLVM toolchain integration, and executable samples.

The emulator is a non-owning executable consumer of the surrounding ISA
repository. Static encodings and operand/EA grammar come from `../isa/defs`;
handwritten Sail under `../sail` owns executable architectural behavior. The
checked-in Rust decode table is generated from the definitions and does not
independently define the ISA.

## Workspace Layout

- `bedrock-isa`: instruction word, prefix, operand, and decode skeletons.
- `bedrock-bus`: byte-addressed bus, RAM, devices, and address-map helpers.
- `bedrock-core`: CPU state, memory translation, exception delivery, integer
  execution, and the initial executable FPU subset used by the samples.
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

The generator derives its input and output locations from its own installed
path, so this freshness check also works from any current directory:

```sh
python3 /path/to/isa-design/emulator/tools/gen_isa.py --check
```

From this directory, the equivalent Rust-only checks are:

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

`samples/tiny_kernel` builds a small kernel with a TTY shell. Shell commands
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
complete LLVM checkout and build, including its headers and libraries. Select
that checkout with `BEDROCK_LLVM_ROOT`:

```sh
export BEDROCK_LLVM_ROOT=/path/to/llvm-bedrock
# Optional executable-directory override for tool calls and sample builds:
export BEDROCK_LLVM_BIN="$BEDROCK_LLVM_ROOT/build/bin"
```

When `BEDROCK_LLVM_ROOT` is unset, full-workspace builds look for an external
`../llvm-bedrock` checkout beside the ISA repository. `BEDROCK_LLVM_BIN` alone
only overrides executable tool lookup; it does not supply the LLVM headers and
libraries required for full-workspace validation. The toolchain wrapper runs:

```sh
llvm-mc -triple=bedrock-unknown-unknown -filetype=obj program.s -o program.o
ld.lld -m elf64bedrock program.o --image-base=0 -Ttext=0x1000 -o program.elf
llvm-objdump -d --no-show-raw-insn program.elf
```
