# Fixed 3D Sample

Integer-only fixed-point wireframe cube renderer for the Bedrock emulator.
The sample identity maps RAM, maps framebuffer VRAM into the high virtual MMIO
window, enables page translation with `SWPT.D`, then animates a rotating cube
using Q8 sine/reciprocal tables and Bresenham line drawing.

Build from the workspace root:

```sh
export BEDROCK_LLVM_BIN=/path/to/llvm-bedrock/build/bin
"$BEDROCK_LLVM_BIN/clang" \
  -target bedrock-unknown-unknown \
  -ffreestanding -nostdlib -O2 \
  -Wl,-Ttext=0x1000 -Wl,--image-base=0 \
  samples/fixed3d/main.c \
  -o /private/tmp/bedrock-fixed3d.elf
```

Run it in the GUI:

```sh
cargo run -p bedrock-gui
```

Load `/private/tmp/bedrock-fixed3d.elf`, set `steps/frame` high enough for
animation, then press `Run`.
