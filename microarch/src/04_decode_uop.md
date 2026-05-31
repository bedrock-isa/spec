## Decode and Uop Translation

The decoder maps architectural instructions into a small internal uop language.
The baseline implementation may execute these uops immediately, while a later
core may queue or rename them.

Typical examples:

```text
MOV.L [A0 + D1 * 4], D0
  -> AGU
  -> LOAD
  -> WRITE_REG

ADD.L [A0], D1
  -> AGU
  -> LOAD
  -> ALU_ADD
  -> WRITE_REG
  -> WRITE_FLAGS

MOV.L D0, [A1]
  -> AGU
  -> STORE

MOV.L [src], [dst]
  -> AGU_SRC
  -> LOAD
  -> AGU_DST
  -> STORE
```

Memory-memory instructions remain architectural instructions, but internally
they are decomposed into ordered uops. The decoder must preserve instruction
identity so exceptions report the architectural instruction and, for repeat
forms, the dynamic instruction instance within the repeated stream.

