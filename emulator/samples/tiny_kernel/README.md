# Tiny Kernel Sample

This sample is a small multi-file C kernel, shell, and a set of embedded
separate ELF user applications with thin assembly entry stubs in `boot.s`.

Build it with the Bedrock LLVM toolchain:

```sh
make -C samples/tiny_kernel
```

The default output is `samples/tiny_kernel/build/tiny_kernel.elf`. To also
write an objdump listing:

```sh
make -C samples/tiny_kernel disasm
```

Set `BEDROCK_LLVM_BIN=/path/to/llvm-bedrock/build/bin` or
`BEDROCK_LLVM_ROOT=/path/to/llvm-bedrock` to select the external toolchain. If
neither is set, the Makefile looks for `../llvm-bedrock/build/bin` beside the
ISA repository.

- `kernel.c` configures the `SPC` syscall entry and the common `EPC` event
  entry, bounds-checks supervisor code and event stacks through their segment
  images, and enables paging before entering the shell. `SDS` stays flat
  because kernel C address arithmetic can materialize non-address intermediate
  values through `LEA`.
- `memory.c` owns a 4 KiB page allocator, four-level page-table builder, the
  shared user-image frame arena, and PTCR/ASID switching. Kernel code is RX,
  kernel data and MMIO are RW/NX, and supervisor mappings omit the user bit.
- `process.c` tracks the shell process plus one process record per embedded
  app, syscall counters, yield points, fault recovery, and page checksum
  markers.
- `shell.c` is the user-mode shell. It requests keyboard and TTY framebuffer
  operations through syscalls, echoes printable ASCII as typed, and dispatches
  case-insensitive commands by asking the kernel to load an embedded user ELF.
- The linker isolates shell text, read-only data, TLS, and stack on separate
  pages. The shell address space maps only those pages as user-accessible and
  binds its TLS block to `GS0`.
- Framebuffer writes and keyboard reads use inline volatile C MMIO accesses;
  assembly is reserved for privilege, syscall, and event boundaries.
- `syscall.c` owns the syscall dispatch path and checksum accounting.
- `user.c` is intentionally empty; user applications live outside the kernel
  image source and are embedded as ELF bytes.
- `../userland/apps` builds the `MATH`, `SORT`, `MEM`, `FAR`, `DEMO`, `FAULT`,
  and `HALT` user ELFs. `../userland/basic` builds the BASIC user ELF. The kernel
  embeds each image as data, loads its PT_LOAD segments on demand, gives it
  separate code/data and stack bounds, runs it in user mode, and returns to the
  shell through `SYSCALL_EXIT` when the app exits normally.
- `display.c` draws a plain TTY-style text surface on the framebuffer so the
  program can be loaded in the GUI and inspected by eye without decorative
  panels or animated bars.

After boot, the screen starts at pixel `(0, 0)` with a `>` prompt. Focus the
display and type one of these commands followed by Enter:

- `MATH`: runs integer-heavy Fibonacci/mixing arithmetic in user mode and
  prints the low Fibonacci, mix, and result bytes.
- `SORT`: sorts a local byte array in its own user stack segment and prints
  min, max, and checksum bytes.
- `MEM`: exercises local stack/data memory in its own user process and prints
  first, last, and checksum bytes.
- `FAR`: installs a translated window in `GS1`, fills and transforms a
  page-aligned memory bank through explicitly segment-qualified accesses, then
  prints the input edges, output edges, checksum, and PASS/FAIL.
- `PFAULT`: reads a supervisor-only kernel page through a disabled segment
  image; the kernel records a paging permission fault, terminates the app, and
  returns to the shell.
- `SFAULT`: reads outside the app's DS window; the kernel records a segment
  bounds fault, terminates the app, and returns to the shell.
- `DEMO`: sends the payload stream through `SYSCALL`, periodically yields
  through the syscall table, and prints the resulting checksum/yield summary.
- `BASIC`: executes the embedded separate ELF user application and enters a
  small BASIC-like prompt. `LIST` prints the program, `RUN` performs integer
  and double-precision FPU arithmetic, `PRINT` repeats the last decimal result,
  and `EXIT` returns to the shell.
- `FAULT`: deliberately triggers a user-mode `RDCR` privilege fault and
  resumes through `ERET`.
- `HALT`: executes `BKPT` from user mode and lets the kernel breakpoint handler
  halt the emulator.
- `HELP`, `CLEAR`, `STATS`: small shell utility commands.

The framebuffer shows only the shell transcript. A separate RAM marker array is
used by the LLVM integration test as an acceptance check:

- `0x00..0x0f`: syscall handler writes the user payload stream.
- `0x30..0x32`: boot, syscall count, and user arithmetic markers.
- `0x40..0x44`: privilege-fault and `ERET` markers.
- `0x50..0x55`: breakpoint handler and checksum markers.
- `0x56..0x5e`: process payload count, yield count, allocated page count,
  process state, user mirror, page checksum, last yield ticket, and bad syscall
  count.
- `0x60..0x63`: shell ready, command count, last command, and fault-return
  markers.
- `0x68..0x6a`: `MATH`, `SORT`, and `MEM` user-program result markers.
- `0x6f`: `FAR` user-program checksum marker; the expected value is `0xaa`.
- `0x6b..0x6c`: TTY scroll syscall rows and marker signature.
- `0x70..0x78`: embedded app ELF loader, process switch, segment, and exit code
  markers.
- `0x79..0x7a`: last page-fault reason and cumulative page-fault count.
- `0x64..0x65`: low bytes of the configured supervisor segment window.
- `0x66..0x67`: low bytes of the configured GS0 user TLS segment window.

Each shell/application process has a distinct four-level root and uses its PID
as the ASID. Embedded applications keep their ABI virtual base at `0x80000`,
but their PT_LOAD pages are copied into a reusable physical arena and mapped as
RXU or RWU from the ELF flags. The active app is the only runnable application,
so the arena is cleared and reused on every exec while page-table roots remain
process-specific.

Exceptions enter through the common `EPC`/`ECS`/`EDS` state. Page faults use
event ID `0x09` and the `FSS`/`FSP` exception stack. The low byte of
`error_code` is the fault-reason code; bits 9..8 select none, read, write, or
execute access, bit 10 records the user-domain path, and bits 24 and 25 mark
the effective and linear addresses as valid. `fault_ea`, `fault_linear`, and
`fault_aux` carry the pre-segment address, post-segment address, and auxiliary
fault metadata.
