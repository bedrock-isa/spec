## Pipeline Overview

The baseline pipeline is organized around explicit instruction packets:

```text
instruction fetch
  -> word0 predecode
  -> prefix and payload collection
  -> instruction packet queue
  -> decoder / uop translator
  -> in-order issue
  -> execute / address generation / memory
  -> retirement
```

The baseline core is in-order from issue through retirement. Execution may use
multi-cycle units, but architectural state is updated only at defined retirement
points. A simple scoreboard may hold issue until source operands and structural
resources are available; it does not imply register renaming or out-of-order
execution.

Later high-performance implementations may keep the same logical boundaries
while adding more aggressive machinery:

```text
fetch block
  -> predecode metadata
  -> instruction packet queue
  -> uop translation/cache
  -> rename
  -> issue queues
  -> execution clusters
  -> reorder buffer retirement
```

That path is explicitly outside the initial RTL scope.

The important invariant is that fetch and decode produce a precise linear stream
of architectural instruction instances, even when later implementation stages
execute internally in a different order.
