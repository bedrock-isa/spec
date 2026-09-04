# Echo Sample

Keyboard MMIO events are rendered as 8x8 RGB332 glyphs into the framebuffer.
The sample maps framebuffer and keyboard MMIO into a high virtual address range,
enables page translation, then echoes printable ASCII input to the display.

Build from the ISA repository root:

```sh
BEDROCK_LLVM_BIN=/path/to/llvm/bin make samples
```

Run it in the GUI from `emulator/`:

```sh
cargo run -p bedrock-gui
```

Load `output/samples/echo.elf`, press `Run`, then send text from the
keyboard panel.
