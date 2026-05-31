# Bedrock Microarchitecture Notes

This directory contains source fragments for Bedrock microarchitecture design
notes. The generated document is intentionally separate from the ISA reference:
it describes candidate implementation structure, not architectural software
semantics.

Build the synthesized document with:

```sh
make -C microarch doc
```

The output is written to:

```text
build/microarch/bedrock_microarchitecture.md
```

