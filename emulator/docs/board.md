# Bedrock Emulator MVP Board

The CPU core does not know about concrete devices. It reads and writes through
the `bedrock-bus` traits. `bedrock-machine` owns the MVP board map and routes
addresses to RAM or MMIO devices.

## Address Map

| Range | Device |
| --- | --- |
| `0x0000_0000..0x0010_0000` | RAM, 1 MiB |
| `0x00F0_0000..0x00F1_0000` | Framebuffer VRAM window |
| `0x00F1_0000..0x00F1_0100` | Display registers |
| `0x00F2_0000..0x00F2_0100` | Keyboard registers |

## Display

The display device uses a fixed `320x200` framebuffer with one byte per
pixel in RGB332 format. The visible VRAM payload is 64,000 bytes. The rest of
the 64 KiB VRAM window is unmapped padding.

Display registers are byte-addressed:

| Offset | Access | Meaning |
| --- | --- | --- |
| `0x00..0x03` | read-only | width as little-endian `u32` |
| `0x04..0x07` | read-only | height as little-endian `u32` |
| `0x08..0x0B` | read-only | pixel format ID as little-endian `u32`: `1` (RGB332) |
| `0x0C..0x0F` | read/write | control as little-endian `u32`, bit 0 enables output |
| `0x10..0x17` | read-only | dirty sequence as little-endian `u64` |

## Keyboard

The keyboard device exposes a small event FIFO. Key events are `u32`
values:

| Bits | Meaning |
| --- | --- |
| `0..15` | key code: printable ASCII `0x0020..0x007e`; Backspace `0x0008`, Tab `0x0009`, Enter `0x000d`, Escape `0x001b`, Delete `0x007f`; arrows `0x0101..0x0104`; Insert/Home/End/Page Up/Page Down `0x0110..0x0114`; Copy/Cut/Paste `0x0120..0x0122`; F1..F35 `0x0201..0x0223` |
| `16` | pressed when set, released when clear |
| `17` | Shift modifier |
| `18` | Control modifier |
| `19` | Alt modifier |
| `20` | Command modifier |
| `21..31` | unused |

Keyboard registers are byte-addressed:

| Offset | Access | Meaning |
| --- | --- | --- |
| `0x00..0x03` | read-only | status as little-endian `u32`, bit 0 data available, bit 1 overflow |
| `0x04..0x07` | read-only | data as little-endian `u32`, reading byte 0 pops one event |
| `0x08..0x0B` | write-only | control byte 0, bit 0 enable, bit 1 clear FIFO |

## ELF Loading

The loader follows `bedrock-elf-abi.pdf` for the language-neutral Bedrock ELF ABI:

- ELF64, little-endian, `EM_BEDROCK = 0xffb0`.
- `ET_EXEC` and executable `ET_DYN` are accepted.
- `e_flags` must be zero.
- `e_ident[EI_VERSION]` and ELF header `e_version` must be current.
- ELF header size must be 64 bytes, program header size 56 bytes, section header size 64 bytes.
- `PT_LOAD` segments are loaded at `p_vaddr` for `ET_EXEC`.
- `PT_LOAD` segments are loaded at `load_base + p_vaddr` for `ET_DYN`.
- `PT_LOAD` flags must use ABI-defined `PF_R`, `PF_W`, and `PF_X` bits, and loadable mappings must be readable.
- Metadata program headers emitted by LLD, including `PT_PHDR` and `PT_GNU_STACK`, are accepted without mapping memory.
- The CPU is reset to `e_entry` for `ET_EXEC`, or `load_base + e_entry` for `ET_DYN`, in privileged `STATUS.PM` boot state.
- `p_filesz..p_memsz` is zero-filled for BSS.
