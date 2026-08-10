# Echo Sample

Keyboard MMIO events are rendered as 8x8 RGB332 glyphs into the framebuffer.
The sample maps framebuffer and keyboard MMIO into a high virtual address range,
enables page translation, then echoes printable ASCII input to the display.

Build from the workspace root:

```sh
export BEDROCK_LLVM_BIN=/path/to/llvm-bedrock/build/bin
"$BEDROCK_LLVM_BIN/clang" \
  -target bedrock-unknown-unknown \
  -ffreestanding -nostdlib -O2 \
  -Wl,-Ttext=0x1000 -Wl,--image-base=0 \
  samples/echo/main.c \
  -o /private/tmp/bedrock-echo.elf
```

Run it in the GUI:

```sh
cargo run -p bedrock-gui
```

Load `/private/tmp/bedrock-echo.elf`, press `Run`, then send text from the
keyboard panel.
