# Fixed 3D Sample

Integer-only fixed-point wireframe cube renderer for the Bedrock emulator.
The sample identity maps RAM, maps framebuffer VRAM into the high virtual MMIO
window, enables page translation with `SWPT.D`, then animates a rotating cube
using Q8 sine/reciprocal tables and Bresenham line drawing.

Build from the ISA repository root:

```sh
BEDROCK_LLVM_BIN=/path/to/llvm/bin make samples
```

Run it in the GUI from `emulator/`:

```sh
cargo run -p bedrock-gui
```

Load `output/samples/fixed3d.elf`, set `steps/frame` high enough for
animation, then press `Run`.
