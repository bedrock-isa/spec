# Bedrock

Bedrock is a 64-bit instruction set architecture and systems-software specification. The specification covers the programmer-visible architecture, a 64-bit ELF environment, and an LP64 C ABI.

## A Bedrock instruction in one glance

```asm
REP R1, ADD.Q [DS:R2 + R3++ * 8 + 32], R4
```

Repeat the scalar `ADD.Q` body `R1` times: add the 64-bit value at `DS:(R2 + R3 * 8 + 32)` to `R4`, increment the element index `R3` after every committed iteration, and retain a precise restart boundary if an iteration faults.

For an overview of the architecture, read the [Architectural Introduction](docs/introduction.md).

## License

This project is licensed under the [Apache License 2.0](LICENSE).
