# Allocation Source Format

The allocation YAML files are the source of truth for opcode payload assignment.
They are intentionally small and regular so they can be validated, rendered into
documentation, and later consumed by encoder/decoder generators.

Each file describes one opcode payload class. Instruction stream framing maps
classes to payload widths as follows:

```text
extrashort  byte0[7]=0                              7-bit payload, 1 byte
short       byte0[7:6]=10                          14-bit payload, 2 bytes
medium      medium opcode-length pattern           18-bit payload, 3-byte opcode
long        long opcode-length pattern             26-bit payload, 4-byte opcode
extralong   extralong opcode-length pattern        34-bit payload, 5-byte opcode
```

Extended instruction byte0[5:2] encodes the total instruction length as
`3 + L` bytes. The encoded length must be large enough to contain the selected
opcode class: 3 bytes for medium, 4 bytes for long, and 5 bytes for extralong.
Long and extralong opcode length patterns select those classes directly.

Each YAML file has this shape:

```yaml
class: medium
payload_bits: 18
namespace:
  - "??????????????????"   # optional; class defaults are inferred when omitted
entries:
  - id: medium.example
    bits: "00zzssssdddd????"
    text: "EXAMPLE.X Rn(s), Rn(d)"
    fields:
      z: {kind: size, width: 2}
      s: {kind: rn, width: 4}
      d: {kind: rn, width: 4}
    constraints:
      - {field: c, allow: [0x2..0xf], reason: condition_true_false_reclaimed}
      - {field: e, exclude: rn_direct, reason: canonical_form_reclaim}
      - {destination: true, exclude: immediate, reason: invalid_destination}
```

`namespace` is optional. When omitted, tools infer the class namespace from the
opcode-length class: `medium` defaults to the `0`, `10`, `110`, and `1110`
payload-selector prefixes, `long` defaults to the `111100`, `111101`, and
`111110` payload prefixes, `extralong` defaults to the `111111` payload prefix,
and other classes default to the full payload space.

`bits` uses `0` and `1` for fixed opcode bits. Any other character is a named
field bit, except `?`, which is an anonymous wildcard. Repeating the same field
letter concatenates those bits in left-to-right order.

`text` is only the instruction form. Do not append semicolon comments such as
reclaim, condition-code, or immediate-range notes to `text`; those notes are
rendered from structured `constraints` so every generated table uses the same
format. Use an explicit `notes` list only for comments that cannot be expressed
as constraints. The allocation validator rejects semicolons in `text`.

Every item under `entries` is an allocated instruction form. There is no
reserved-entry type; payload values that are not covered by an entry are
reported as remaining reserved/unassigned space. Wider opcode classes are
selected by their own class length patterns and namespaces.

Supported constraint forms:

```text
field + allow     only listed field values are assigned
field + exclude   matching field values are reclaimed from this entry
destination       apply the exclusion to the destination EA field
```

Supported value predicates:

```text
rn_direct   EA value 0x00..0x0f
sp_direct   EA value 0x68
reg_direct  rn_direct or sp_direct
immediate   EA value 0x6c..0x6f
```

Ranges use inclusive `lo..hi` syntax. Numeric bounds can be decimal, binary, or
hexadecimal.

Rendered constraint notes use these forms:

```text
allow cccc=0010..1111
allow cccc=0000,0010..1111
allow iiiiiiii=00000001..11111111
reclaim e.rn
reclaim e.sp
reclaim e.reg
dst !imm
```

## Reports

Generate occupancy reports from the allocation source with:

```sh
python3 isa/tools/gen_alloc_report.py
```

The default outputs are written under `build/reports/`:

```text
encoding_allocation_report.md
encoding_allocation_report.json
encoding_allocation_report_classes.csv
encoding_allocation_report_entries.csv
encoding_allocation_report_mnemonics.csv
```

The report lists class-level occupancy, reclaim reasons, mnemonic totals, and
per-form assigned/reclaimed slot counts.

## Editing Aid

Use the allocation editor helper while choosing or moving encodings:

```sh
python3 isa/tools/alloc_edit.py summary
python3 isa/tools/alloc_edit.py legend --color always
python3 isa/tools/alloc_edit.py holes long --min-wildcards 15
python3 isa/tools/alloc_edit.py check long 11110000111ccccrrrreeeeeee
python3 isa/tools/alloc_edit.py entries long --leading 1111000011
python3 isa/tools/alloc_edit.py entries medium --leading 000010 --show-reserved
```

`holes` lists aligned clean-free blocks by default. Reclaimed slots are excluded
unless `--include-reclaimed` is passed. `check` accepts the same field-letter
patterns used by the YAML files and treats non-binary letters as wildcards.
When checking a move of an existing entry, pass `--ignore-entry <id>` so the
entry does not collide with itself.
`entries --show-reserved` inserts computed `reserved.*` rows for payload slots
not covered by an entry or reclaim constraint, and `reclaimed.*` rows for
unclaimed slots excluded by entry constraints. `--reserved-limit` can cap
each synthetic row class.
`holes` and `entries --show-reserved` minimize wildcard covers with PyEDA
Espresso and verify that the emitted patterns cover the exact target set without
overlap.

On the local Anaconda Python 3.13 install, PyEDA may need this build flag:

```sh
CFLAGS='-Wno-incompatible-function-pointer-types' /opt/homebrew/anaconda3/bin/python3 -m pip install pyeda
/opt/homebrew/anaconda3/bin/python3 isa/tools/alloc_edit.py holes long
```

`entries`, `check`, and `legend` color field letters by field kind when stdout
is a terminal. Use `--color always` or `--color never` to override automatic
detection. The color map is:

```text
size       z
rn         r/s/d/b/etc.
freg       f/l/r/s/d/etc.
ea7        e/s/d 7-bit EA fields
condition  c
immediate  i
bits       unclassified field bits
```
