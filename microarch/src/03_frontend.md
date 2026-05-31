## Frontend and Word-0 Predecode

Word 0 is the natural frontend boundary. The predecoder extracts:

- `P`, the prefix-present bit,
- `L`, the encoded instruction length,
- total instruction length in words,
- the 12-bit primary payload,
- HALT and ILLEGAL sentinel payloads.

Instruction boundaries are computed without walking operand encodings. This
keeps fetch simple even when an instruction contains an extended EA descriptor or
overlong padding.

The frontend should produce an instruction packet containing at least:

```text
pc
word0
length_words
prefix_present
prefix_word_valid
prefix_word
payload_words
primary_payload
sentinel_class
```

Later implementations may cache predecode metadata beside instruction memory:

- instruction start,
- instruction length,
- prefix-present,
- branch/control hint,
- extended descriptor hint,
- REPG start or ENDG hint.

These hints are implementation metadata only. They must be recoverable from the
architectural instruction stream.

