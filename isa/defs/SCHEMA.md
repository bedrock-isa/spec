# YAML Schema Contract

The Bedrock YAML schema is frozen at version 0. This file displays the complete
shape accepted by `isa/tools/defs_schema.py`, including nested records and
discriminated variants. `schema.lock` pins the SHA-256 digests of both files.

Changing an allowed field, required field, value type, enum, path rule, or
cross-field invariant is a schema change. While the project remains unreleased,
keep `SCHEMA_VERSION` at 0 and update this contract, its tests, and
`schema.lock` deliberately. A version increment requires an explicit release
or versioning decision.

## Notation and common rules

```text
field: T             required field
field?: T            optional field
list<T>              YAML sequence
map<string, T>       YAML mapping with arbitrary non-empty string keys
enum(a, b)           one of the listed strings
int[N..M]            integer in the inclusive range; booleans are not integers
T | U                 either type
exactly-one(a, b)    precisely one of the fields is present
```

Every mapping shown below is closed: any unlisted field is rejected. Required
strings are non-empty. Relative references are normalized POSIX paths with no
absolute path or `.`/`..` component. Lists marked unique reject duplicates.

## 1. `instruction.yaml`

```text
InstructionDocument {
  mnemonic: string matching [A-Za-z][A-Za-z0-9]*
  title: string
  summary: string
  description: string
  attributes: InstructionAttributes
  flag_effects?: map<enum(FLAGS, FFLAGS), map<flag-name, string>>
  additional_assembler_syntax?: list<string, unique>
  additional_description?: relative-path ending in .tex
}

InstructionAttributes {
  class: string
  family: string
  privilege: enum(unprivileged, supervisor, any)
  repeat?: list<enum(REP, REPcc, REPG, REPGF), unique>
}
```

`FLAGS` accepts `Z`, `N`, `C`, and `V`; `FFLAGS` accepts `NV`, `DZ`, `OF`,
`UF`, and `NX`. Each present bank is non-empty. Renderers use the listed
architectural flag order rather than YAML mapping order.

## 2. `encodings.yaml`

```text
EncodingsDocument {
  forms: list<EncodingForm>
}

EncodingForm {
  id: string matching [a-z][a-z0-9_]*\.[a-z0-9_.]+
  class: string
  bits: string containing only 0, 1, ?, and lowercase field markers
  syntax: string
  operands?: list<EncodingOperand>
  sizes?: list<string, unique>
  fields?: map<one-character marker, EncodingField>
  constraints?: list<EncodingConstraint>
  notes?: list<string>
}

EncodingOperand {
  name: string
  type: string
  access: enum(read, write, read_write, address)
  field?: one-character marker occurring in EncodingForm.bits
  domain?: enum(user)
}

EncodingField {
  type: string
}

EncodingConstraint {
  field: one-character marker occurring in EncodingForm.bits
  reason: string
  exactly-one(
    allow: list<int | string>,
    exclude: string
  )
}
```

Form IDs are unique within a document and begin with `class + "."`. Operand
field markers are unique. Operand fields plus `fields` declare every symbolic
marker in `bits` exactly once; `0`, `1`, and `?` are not declared markers.

## 3. `instructions.yaml`

```text
InstructionSetIndex {
  title: string
  include: non-empty list<relative-path, unique>
  introduction?: relative-path ending in .tex
}
```

The `include` sequence is also the document order.

## 4. Extension documents

`extensions.yaml`:

```text
ExtensionCatalog {
  extensions: list<relative-path, unique>
}
```

`extension.yaml`:

```text
ExtensionManifest {
  name: string
  instructions?: relative-path
  operands?: relative-path
  registers?: relative-path
  sizes?: relative-path
  extensions?: list<relative-path, unique>
  availability?: ExtensionAvailability
}

ExtensionAvailability {
  cpuid: CpuidAvailability
}

CpuidAvailability {
  feature: string
  class: int[0..]
  leaf: int[0..]
  index: int[0..]
  bit: int[0..63]
}
```

## 5. `operands.yaml`

```text
OperandRegistry {
  operand_types: map<string, OperandType>
}

OperandTypeCommon {
  kind: OperandKind
  field_width: int[0..]
}

OperandKind = enum(
  register,
  fixed_register,
  effective_address,
  enum,
  ea_immediate,
  bitmap,
  immediate,
  relative_immediate
)
```

`OperandType` is the following closed discriminated union. Fields belonging to
another variant are rejected.

```text
kind: register {
  kind: register
  field_width: int[0..]
  register_group: string
}

kind: fixed_register {
  kind: fixed_register
  field_width: int[0..]
  register: string
}

kind: effective_address {
  kind: effective_address
  field_width: int[0..]
  encoding_ref: string
}

kind: enum {
  kind: enum
  field_width: int[0..]
  exactly-one(
    values: list<OperandEnumValue>,
    values_ref: string
  )
  reserved_values?: list<OperandEnumValue>
  result_bits_format?: string
}

kind: ea_immediate {
  kind: ea_immediate
  field_width: int[0..]
  encoding_ref: string
}

kind: bitmap {
  kind: bitmap
  field_width: int[0..]
  bits: list<OperandBit>
}

kind: immediate | relative_immediate {
  kind: enum(immediate, relative_immediate)
  field_width: int[0..]
  signed: bool
  operation_size_extension?: string
}

OperandEnumValue {
  value: int | string
  name: string
  registers?: list<string, unique>
  value_bits?: string
}

OperandBit {
  bit: int[0..field_width-1]
  name: string
}
```

Enum/reserved values and names are unique within their lists and combined enum
numeric/string values do not overlap. Bitmap bit numbers and names are unique.

## 6. `sizes.yaml`

```text
SizeRegistry {
  size_codes: map<string, SizeCode>
  size_kinds: map<string, SizeKind>
}

SizeCode {
  suffix: string beginning with .
  bytes: int[1..]
}

SizeKind {
  field: one lowercase character
  values: non-empty list<SizeValue>
  reserved_values?: list<ReservedSizeValue>
}

SizeValue {
  value: int[0..]
  code: string
}

ReservedSizeValue {
  value: int[0..]
  name: string
}
```

Values are unique within each list and cannot overlap reserved values.

## 7. `registers.yaml`

```text
RegisterRegistry {
  registers: map<string, RegisterGroup>
}

RegisterGroup {
  entries: non-empty list<RegisterEntry>
}

RegisterEntry {
  name: string
  width: int[1..]
  encoding?: int[0..]
  role?: string
  description?: string
}
```

Names and present encodings are unique within a register group.

## 8. `conditions.yaml`

```text
ConditionRegistry {
  conditions: non-empty list<ConditionDefinition>
}

ConditionDefinition {
  name: string
  value: int[0..]
  expression: string
  aliases?: list<string, unique>
}
```

Condition values are unique. Every primary name and alias shares one global
unique namespace.

## 9. `ea.yaml`

```text
EaRegistry {
  payloads: map<string, EaPayload>
  compact: CompactEaSection
  ext0: Ext0EaSection
}

EaPayload {
  kind: string
  field_width: int[1..]
  signed: bool
}

CompactEaSection {
  field_width: int[1..]
  forms: list<CompactEaForm>
}

CompactEaForm {
  name: string
  pattern: BitPattern of exactly CompactEaSection.field_width bits
  syntax: string
  kind: string
  fields?: map<one lowercase marker, EaField>
  segment?: string
  payload?: string
  base?: string
  register?: string
  descriptor?: string
}

Ext0EaSection {
  kind: string
  forms: list<Ext0EaForm>
}

Ext0EaForm {
  name: string
  pattern: non-empty list<BitPattern of exactly 8 bits>
  syntax: string
  fields?: map<one lowercase marker, EaField>
  segment?: string
  base?: string
  update?: EaUpdate
}

EaField {
  type: string
  role: string
}

EaUpdate {
  target: declared field marker
  mode: enum(postincrement, predecrement)
}

BitPattern = string containing only 0, 1, and lowercase markers
```

Form names are unique per section. Every pattern marker has exactly one field
declaration and vice versa. Compact `payload` values reference a declared
`payloads` key.

## 10. `isa/abi/plt_golden_vectors.yaml`

```text
AbiVectorsDocument {
  ordinary_plt: OrdinaryPlt
}

OrdinaryPlt {
  entry_size: int[1..]
  alignment: int[1..]
  instruction: AbiInstruction
  relocation: AbiRelocation
  padding: AbiPadding
  got_slot: AbiGotSlot
  relocation_vectors: list<AbiRelocationVector>
}

AbiInstruction {
  assembly: string
  offset: int[0..]
  opcode_bytes: list<int[0..255]>
  total_bytes: int[1..]
  displacement: AbiDisplacement
}

AbiDisplacement {
  offset: int[0..]
  width_bits: int[1..]
  byte_order: string
}

AbiRelocation {
  type: string
  place: string
  addend: int
  calculation: string
  effective_displacement: string
}

AbiPadding {
  offset: int[0..]
  length: int[0..]
  byte: int[0..255]
}

AbiGotSlot {
  size: int[1..]
  alignment: int[1..]
  contents: string
  immutable_after_publication: bool
}

AbiRelocationVector {
  entry_address: int[0..]
  got_slot_address: int[0..]
  place: int[0..]
  addend: int
  encoded_little_endian: list<int[0..255]>
  exactly-one(
    result: int,
    result_signed: int
  )
}
```

## 11. `isa/memory_model/validation.yaml`

```text
MemoryValidationDocument {
  status: string
  target: MemoryValidationTarget
  litmus_families: list<LitmusFamily>
  failure_action: list<string, unique>
}

MemoryValidationTarget {
  afence_is_full_cumulative: bool
  one_global_sc_order: bool
  isolated_fenced_scalar_is_sc: bool
  failed_seqcst_cmpxchg_is_sc_load: bool
  compare_exchange_uses_order_join: bool
  failed_release_component_creates_release_sequence: bool
}

LitmusFamily {
  id: string, unique within litmus_families
  purpose: string
}
```

## Cross-document validation after decoding

The strict decoder fixes document shape and local invariants. The validators
then enforce the following references and global invariants:

- extension manifests, instruction indexes, introduction TeX, and instruction
  detail TeX references exist;
- instruction directory name equals `mnemonic`, indexes cover every definition
  exactly once, and mnemonics are globally unique;
- operand and size names are registered, encoding marker widths equal their
  primitive widths, and EA write destinations reclaim immediate encodings;
- CPUID feature names and `(class, leaf, index, bit)` positions are unique;
- encoding IDs are globally stable, class names and bit widths match the fixed
  grammar in `isa/tools/encoding_architecture.py`, and concrete opcode claims
  do not overlap.
