# ISA Missing-Reference Recovery Plan

Status: implemented and verified, 2026-07-13.

## Constraints

- Do not add architectural YAML files or modify `isa/defs/manifest.yaml`.
- Keep machine definitions limited to data used by encoders, decoders, or validators.
- Keep selector tables, register layouts, reset rules, and other reader-facing reference material in TeX.
- Do not generate C from YAML. Maintain public C constants by hand.
- Do not restore removed opcode, prefix, DBANK, or instruction designs.
- Do not write to `.git`; package changes as sequential patches under `build/commits`.

## Instruction Reference Extension

An instruction may name a human-authored TeX fragment through `doc.description_tex`. The path is relative to the ISA
template directory, must end in `.tex`, and may not be absolute or escape the template root. The generator inserts
the fragment at full width after condition-code/status information and before Instruction Forms.

RDCR and WRCR share the control-register fragment. RDPMC uses the performance-counter fragment.

## Recovery Decisions

| Area | Status | Current treatment |
|---|---|---|
| CR namespace | retained/redesigned | shared RDCR/WRCR TeX fragment |
| PTC/RDPTC | superseded | PMC selector 0x1100 and RDPMC counter ID 2 |
| interrupt stack sets | retained | interrupt and privileged-model TeX |
| boot state | retained/clarified | RESET description and CR TeX |
| STATUS/FPU state | retained | state-register TeX |
| CPUID/SAVE layout | retained/currentized | existing TeX templates |
| old prefixes/opcodes | discarded | current allocation only |
| DBANK | discarded | not restored |
| old ABI YAML | superseded | current ABI TeX |

## Patch Series

1. Support safe, full-width instruction description fragments.
2. Restore the CR and performance-counter reference, instruction behavior, and manually maintained C constants.
3. Restore interrupt, reset, translation, and FPU-state documentation.
4. Recover CPUID and SAVE/RESTORE documentation.
5. Close stale references, run all checks, and package recovery-only patches and commit messages.

## Completion Criteria

- [x] No new YAML file and no manifest change.
- [x] No YAML-to-C generation.
- [x] RDCR and WRCR show the same full-width CR reference; RDPMC shows its counter reference.
- [x] PMC uses selector 0x1100; no PTC hole or retired-selector rule remains.
- [x] Manual C constants match the published instruction reference.
- [x] Reset, interrupt, translation, FPU, CPUID, and SAVE/RESTORE descriptions are mutually consistent.
- [x] Definition, allocation, ISA-join, ABI, unit, and C compile checks pass.
- [x] ISA LaTeX, GitHub-Flavored Markdown, and the 437-page PDF build successfully.
- [x] Rendered reference pages have no clipping, overflow, or instruction-field nesting defects.
- [x] Every patch applies sequentially to a clean HEAD snapshot without writing to `.git`.
