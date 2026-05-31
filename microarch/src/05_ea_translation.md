## Effective Address and Translation Boundary

Effective-address calculation and address translation are separate concerns.

```text
EA decode
  -> base/index/displacement calculation
  -> architectural EA
  -> segment pre-translation
  -> linear address
  -> optional page translation
  -> memory-system address
```

The AGU owns architectural EA calculation:

- register-direct EA selection,
- base register selection,
- D-register index selection,
- index sign-extension mode,
- scale application,
- displacement addition,
- immediate and absolute payload collection.

The memory translation block owns:

- segment selection,
- disabled/translated/bounds-only segment behavior,
- canonical checking when paging is enabled,
- TLB lookup and page-table walk,
- PTE permission checks,
- memory-system address production.

This split keeps integer address arithmetic testable before the MMU is complete
and gives a later implementation room for multiple AGUs feeding a shared
translation pipeline.

