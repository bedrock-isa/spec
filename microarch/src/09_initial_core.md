## Initial RTL Core Plan

The first implementation should grow in small, testable blocks:

1. word-0 predecode,
2. instruction boundary scanner,
3. prefix word collection,
4. instruction packet queue,
5. primary compact decoder skeleton,
6. EA decoder and AGU for register and simple memory forms,
7. integer ALU and flags,
8. load/store path with a simple memory model,
9. branch/control transfer support,
10. REP scalar engine,
11. REPG-general scalar engine,
12. segment and paging translation.

Explicitly out of scope for the initial RTL core:

- out-of-order issue and retirement,
- register renaming and a reorder buffer,
- FPU execution,
- SIMD execution units,
- REPG-fast or SIMD/streaming folding.

The current RTL seed covers the first decode-front-end blocks and has started
the shared integer address-generation path. The next useful blocks are the
integer ALU/flags path and a simple ordered load/store path, because they let the
existing full decoder and AGU feed real architectural execution.
