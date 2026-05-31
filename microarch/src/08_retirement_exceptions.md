## Retirement and Exceptions

The baseline core retires architectural state in program order. This makes
precise exceptions straightforward and gives a clear reference model for later
implementations.

Retirement rules:

- ordinary instructions retire as one architectural instruction,
- decomposed uops retire under their parent architectural instruction,
- stores become globally visible only after their fault checks have passed,
- `REP` retires completed iterations before a faulting iteration,
- `REPG` retires the scalar prefix of the linearized grouped stream.

Exception reporting must preserve enough information to restart or emulate the
faulting architectural operation according to the ISA. For grouped repeat faults,
the saved state identifies the faulting instruction instance and reconstructs
the group start using the architectural repeat-fault continuation fields.
`FAULT_AUX.repeat_kind` distinguishes ordinary `REP`/`REPcc`, `REPG-general`,
and `REPG-fast` continuation records. The initial core only produces ordinary
`REP`/`REPcc` and `REPG-general` records; `REPG-fast` is reserved for a future
implementation that actually performs fast grouped execution.
