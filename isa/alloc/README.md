# Allocation Source Format

The allocation YAML files are the source of truth for opcode payload assignment.
They are intentionally small and regular so they can be validated, rendered into
documentation, and later consumed by encoder/decoder generators.

Each file describes one payload class:

```yaml
class: medium
payload_bits: 18
namespace:
  - "??????????????????"   # optional; defaults to the full payload space
entries:
  - id: medium.example
    status: allocated      # allocated | reserved | escape
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

`bits` uses `0` and `1` for fixed opcode bits. Any other character is a named
field bit, except `?`, which is an anonymous wildcard. Repeating the same field
letter concatenates those bits in left-to-right order.

Supported statuses:

```text
allocated  real instruction encoding
reserved   explicitly reserved payload range
escape     escape namespace for a wider payload class
```

Supported constraint forms:

```text
field + allow     only listed field values are assigned
field + exclude   matching field values are reclaimed/reserved
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

