# Architecture Code-Density Comparison

- Optimization: `-Oz` for reference targets
- Bedrock code model: `small`
- Targets: bedrock, m68k, x86_64, aarch64, rv64gc
- Output directory: `../build/compare/arch`

## Target ABI Context

| Target | Toolchain | ISA/options | Code model | PIC/PIE | C ABI |
| --- | --- | --- | --- | --- | --- |
| `bedrock` | `qbe+bedrock-as` | ELF64 | `small` | `none` | Bedrock draft C ABI |
| `m68k` | `m68k-elf-gcc -m68030` | `-m68030` | `absolute32` | `none` | m68k-elf bare-metal C ABI |
| `x86_64` | `x86_64-unknown-linux-gnu` | default | `small` | `none` | System V AMD64 psABI |
| `aarch64` | `aarch64-unknown-linux-gnu` | default | `small` | `none` | AAPCS64 ELF ABI |
| `rv64gc` | `riscv64-unknown-elf` | `-march=rv64gc`, `-mabi=lp64d` | `medlow` | `none` | RISC-V ELF psABI LP64D |

## `bitfield_ops`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 4 | 6 | 5 | 5 | 4 |
| .text bytes | 12 | 22 | 16 | 20 | 12 |
| vs Bedrock | 1.00x | 1.83x | 1.33x | 1.67x | 1.00x |
| Object bytes | 520 | 612 | 728 | 784 | 1000 |

## `block_copy_long`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 7 | 17 | 11 | 9 | 13 |
| .text bytes | 20 | 44 | 28 | 36 | 32 |
| vs Bedrock | 1.00x | 2.20x | 1.40x | 1.80x | 1.60x |
| Object bytes | 664 | 636 | 744 | 808 | 1152 |

## `branch_mix`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 8 | 14 | 14 | 11 | 15 |
| .text bytes | 22 | 32 | 36 | 44 | 38 |
| vs Bedrock | 1.00x | 1.45x | 1.64x | 2.00x | 1.73x |
| Object bytes | 664 | 616 | 744 | 808 | 1144 |

## `call_heavy`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 30 | 22 | 36 | 23 | 31 |
| .text bytes | 104 | 68 | 86 | 92 | 94 |
| vs Bedrock | 1.00x | 0.65x | 0.83x | 0.88x | 0.90x |
| Object bytes | 960 | 808 | 1032 | 1096 | 1496 |

## `clamp_store`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 10 | 24 | 15 | 13 | 17 |
| .text bytes | 30 | 66 | 42 | 52 | 48 |
| vs Bedrock | 1.00x | 2.20x | 1.40x | 1.73x | 1.60x |
| Object bytes | 672 | 652 | 752 | 816 | 1304 |

## `copy_words`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 7 | 17 | 11 | 9 | 13 |
| .text bytes | 20 | 44 | 26 | 36 | 32 |
| vs Bedrock | 1.00x | 2.20x | 1.30x | 1.80x | 1.60x |
| Object bytes | 664 | 628 | 736 | 800 | 1136 |

## `count_threshold`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 8 | 9 | 12 | 11 | 15 |
| .text bytes | 22 | 24 | 29 | 44 | 38 |
| vs Bedrock | 1.00x | 1.09x | 1.32x | 2.00x | 1.73x |
| Object bytes | 664 | 616 | 744 | 816 | 1256 |

## `divmod_heavy`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 16 | 21 | 19 | 17 | 23 |
| .text bytes | 50 | 54 | 50 | 68 | 58 |
| vs Bedrock | 1.00x | 1.08x | 1.00x | 1.36x | 1.16x |
| Object bytes | 744 | 644 | 768 | 832 | 1168 |

## `dot_product`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 7 | 18 | 12 | 10 | 15 |
| .text bytes | 22 | 48 | 32 | 40 | 36 |
| vs Bedrock | 1.00x | 2.18x | 1.45x | 1.82x | 1.64x |
| Object bytes | 664 | 632 | 736 | 800 | 1144 |

## `fir3`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 11 | 24 | 18 | 14 | 21 |
| .text bytes | 38 | 72 | 56 | 56 | 66 |
| vs Bedrock | 1.00x | 1.89x | 1.47x | 1.47x | 1.74x |
| Object bytes | 680 | 648 | 752 | 808 | 1168 |

## `mixed_field_offsets`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 14 | 16 | 11 | 15 | 14 |
| .text bytes | 42 | 52 | 33 | 60 | 34 |
| vs Bedrock | 1.00x | 1.24x | 0.79x | 1.43x | 0.81x |
| Object bytes | 560 | 652 | 752 | 840 | 1032 |

## `multi_fir`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 47 | 84 | 71 | 61 | 79 |
| .text bytes | 156 | 242 | 192 | 244 | 212 |
| vs Bedrock | 1.00x | 1.55x | 1.23x | 1.56x | 1.36x |
| Object bytes | 1104 | 916 | 1152 | 1264 | 1664 |

## `multi_scan`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 53 | 55 | 68 | 63 | 83 |
| .text bytes | 166 | 162 | 161 | 252 | 206 |
| vs Bedrock | 1.00x | 0.98x | 0.97x | 1.52x | 1.24x |
| Object bytes | 1112 | 836 | 1120 | 1272 | 2008 |

## `multi_vector`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 44 | 70 | 65 | 57 | 74 |
| .text bytes | 170 | 206 | 165 | 228 | 190 |
| vs Bedrock | 1.00x | 1.21x | 0.97x | 1.34x | 1.12x |
| Object bytes | 1104 | 872 | 1120 | 1240 | 1784 |

## `pointer_integer_mix`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 22 | 32 | 25 | 20 | 26 |
| .text bytes | 70 | 80 | 70 | 80 | 74 |
| vs Bedrock | 1.00x | 1.14x | 1.00x | 1.14x | 1.06x |
| Object bytes | 824 | 680 | 792 | 856 | 1200 |

## `pointer_sum`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 6 | 9 | 10 | 9 | 12 |
| .text bytes | 20 | 22 | 23 | 36 | 28 |
| vs Bedrock | 1.00x | 1.10x | 1.15x | 1.80x | 1.40x |
| Object bytes | 656 | 600 | 720 | 792 | 1128 |

## `register_pressure`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 25 | 33 | 35 | 29 | 32 |
| .text bytes | 94 | 80 | 109 | 116 | 70 |
| vs Bedrock | 1.00x | 0.85x | 1.16x | 1.23x | 0.74x |
| Object bytes | 792 | 676 | 832 | 896 | 1192 |

## `scale_store`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 10 | 25 | 12 | 11 | 15 |
| .text bytes | 28 | 60 | 33 | 44 | 36 |
| vs Bedrock | 1.00x | 2.14x | 1.18x | 1.57x | 1.29x |
| Object bytes | 672 | 644 | 736 | 808 | 1144 |

## `scan_until_zero`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 8 | 10 | 12 | 11 | 16 |
| .text bytes | 20 | 24 | 28 | 44 | 38 |
| vs Bedrock | 1.00x | 1.20x | 1.40x | 2.20x | 1.90x |
| Object bytes | 664 | 616 | 744 | 816 | 1280 |

## `spill_heavy_loop`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 32 | 44 | 48 | 39 | 49 |
| .text bytes | 128 | 114 | 149 | 156 | 114 |
| vs Bedrock | 1.00x | 0.89x | 1.16x | 1.22x | 0.89x |
| Object bytes | 824 | 712 | 872 | 928 | 1232 |

## `switch_jump_table`

| Case | `bedrock` | `m68k` | `x86_64` | `aarch64` | `rv64gc` |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASM instruction count | 4 | 25 | 5 | 6 | 8 |
| .text bytes | 16 | 82 | 16 | 24 | 20 |
| vs Bedrock | 1.00x | 5.12x | 1.00x | 1.50x | 1.25x |
| Object bytes | 784 | 680 | 976 | 1072 | 1352 |


Artifacts are emitted per case under the output directory.
