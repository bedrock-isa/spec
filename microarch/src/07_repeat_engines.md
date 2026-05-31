## Repeat Engines

### REP and REPcc

`REP` and `REPcc` are best implemented as a repeat uop generator. The repeated
instruction is decoded once, then issued repeatedly while the counter and
condition remain active.

The counter update, condition observation, and fault behavior must match the ISA
definition. Completed iterations commit; a faulting iteration does not commit
the faulting instruction.

### REPG

`REPG` forms a bounded group of ordinary instructions terminated by `ENDG`.
Grouping is a decode/control structure, not a license to change architectural
retirement order.

The architectural dynamic stream is the scalar linearization of the group:

```text
iter0.op0, iter0.op1, ..., iter0.opN,
iter1.op0, iter1.op1, ..., iter1.opN,
...
```

REPG retirement is precise over that linearized stream. On a fault, all dynamic
instruction instances before the faulting instance in that order are committed.
The faulting instance and all later instances are not committed.

The initial core executes `REPG` as this scalar linearized stream. It does not
perform SIMD folding, vectorization, chunked fast execution, or internal
streaming recognition.

`REPG-general` is therefore the only repeat-group execution class implemented by
the first RTL core. The architectural `REPG-fast` continuation class is kept as
a future implementation option, but no fast chunk state is produced by the
initial core.

`REPGF` is an assembler-only contract marker for the fast class. It emits the
same bytes as `REPG`, but the assembler rejects the group if it can see a
fast-class violation such as a selected-counter write, forbidden instruction
class, nested repeat, PC-relative addressing, or grouping-window overflow. The
initial frontend still executes the encoded group through the scalar
`REPG-general` path; `REPGF` is a source-level proof obligation, not an
execution mandate.

Useful implementation strategies include:

- expanding the grouped stream into scalar dynamic instruction instances,
- sharing ordinary integer, AGU, and load/store units with non-repeat code,
- committing completed scalar grouped instructions in architectural order.

Future implementations that add `REPG-fast` or SIMD/streaming folding must still
preserve the scalar linearization as the architectural reference behavior.
