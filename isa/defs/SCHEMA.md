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
  repeat?: RepeatContract
  exceptions?: list<InstructionException>
  flag_effects?: map<enum(FLAGS, FFLAGS), map<flag-name, string>>
  additional_assembler_syntax?: list<string, unique>
  additional_description?: relative-path ending in .tex
}

InstructionAttributes {
  class: string
  family: string
  privilege: enum(unprivileged, supervisor, any)
}

RepeatContract {
  contexts: non-empty list<enum(REP, REPcc, REPG), unique>
  observed?: RepeatObserved
}

RepeatObserved {
  kind: enum(flags, result, source)
  operand?: string
}

InstructionException {
  event: string matching [A-Z][A-Z0-9_]*
  when: string
  forms?: list<form-id, unique>
}
```

`observed` is present exactly when `REPcc` is in `contexts`. `flags` has no
operand; `result` and `source` require an operand name used by the instruction.
Exception event and form references are checked against the architectural event
manifest and the instruction's encoding forms.

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
  destination_overlap?: list<DestinationOverlap>
}

EncodingOperand {
  name: string
  type: string
  access: enum(read, write, read_write, address)
  field?: one-character marker occurring in EncodingForm.bits
  domain?: enum(user)
  ea_role: enum(value, address, control_target) when type = EA
  ea_width: enum(operation_size, B, W, L, Q) when type = EA
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

DestinationOverlap {
  operands: list<string>[exactly 2 distinct writable field operands]
  rule: enum(same_value, illegal_instruction)
}
```

Form IDs are unique within a document and begin with `class + "."`. Operand
field markers are unique. Operand fields plus `fields` declare every symbolic
marker in `bits` exactly once; `0`, `1`, and `?` are not declared markers.
Every EA operand declares both `ea_role` and `ea_width`. `address` role uses
`address` access, `control_target` role uses `read` access, and `value` role
uses `read`, `write`, or `read_write` access. Each operand or field type names
one entry in the merged operand/size field-type registry, and its marker count
in `bits` equals that type's encoded width. An encoded size selector uses an
explicit `size.<SizeKind>` type; its size choices are derived from that kind,
so the form does not also declare `sizes`. Selector-less and fixed-size forms
continue to declare `sizes` directly. `operation_size` requires a resulting
size domain; fixed widths define EXT0 index scale and pre/post-update amount
directly. Reserved size-kind values must be excluded by an `allow` constraint
on the selector field. Field-marker bits need not be contiguous.
Every pair of writable field operands that can designate the same architectural
register has exactly one `destination_overlap` entry.

### Assembly-template language

The following BNF and correspondence rules define canonical template values
for `EncodingForm.syntax` and each element of
`InstructionDocument.additional_assembler_syntax`. In the BNF, quoted strings
are literal text, angle-bracketed names are nonterminals, `|` separates
alternatives, and all repetition is expressed by recursion.

```text
<encoding-form-syntax> ::= <instruction-template>
<additional-assembler-syntax> ::= <instruction-template>

<instruction-template> ::= <instruction-head>
                         | <instruction-head> " " <operand-list>

<instruction-head> ::= <mnemonic-name>
                     | <mnemonic-name> <fixed-size-suffix>
                     | <mnemonic-name> <selected-size-suffix>
                     | <mnemonic-name> <selected-size-suffix> <order-selector>

<selected-size-suffix> ::= "." <size-kind-name> <field-expression>

<order-selector> ::= "/order" <field-expression>

<operand-list> ::= <operand>
                 | <operand> ", " <operand-list>

<operand> ::= <operand-reference>
            | <operand-reference> <field-expression>
            | <decimal-literal>
            | <operand-group>

<operand-reference> ::= <operand-name>
                      | "<" <operand-name> ">"

<field-expression> ::= "(" <field-marker> ")"

<operand-group> ::= "(" <operand-reference> ")"
                  | "{" " " <operand-reference> "..." " " "}"

<decimal-literal> ::= <decimal-digit>
                    | <decimal-digit> <decimal-literal>
<decimal-digit> ::= "0" | "1" | "2" | "3" | "4"
                  | "5" | "6" | "7" | "8" | "9"
```

The grammar uses lexical classes owned by the existing definitions:

- `<mnemonic-name>` has the lexical form of `InstructionDocument.mnemonic`.
  Its owning mnemonic or explicitly recorded alias status is determined by the
  correspondence rules below.
- `<fixed-size-suffix>` is a `SizeCode.suffix`. `<size-kind-name>` is a key in
  the merged size-kind registry. Their spelling and meaning remain owned by
  `sizes.yaml`.
- `<operand-name>` is a case-sensitive identifier beginning with an ASCII
  letter and continuing with ASCII letters, digits, or underscores. Concrete
  operand references are interpreted from the corresponding
  `EncodingOperand.type` and the owning operand and EA registries.
- `<field-marker>` is one lowercase symbolic marker local to the encoding form.
  Its declaration and encoded occurrences remain owned by that form's `bits`,
  `operands`, and `fields`. A field expression binds only that marker.
- Condition names and aliases substituted for `cc` come from
  `conditions.yaml`. The angle-bracket operand reference `<ea>` expands to a
  concrete effective-address spelling owned by `ea.yaml`.

All terminals are case-sensitive. Canonical templates use one explicit space
terminal between a head and its first operand, and comma plus one space between
operands.

The following correspondence rules restrict the BNF to well-formed canonical
templates:

- The base `<mnemonic-name>` of an `EncodingForm.syntax` is exactly the owning
  instruction's registered `mnemonic`. An
  `additional_assembler_syntax` element may instead use the alias spelling
  explicitly recorded by that element for the same instruction.
- A fixed size suffix names exactly the form's one fixed registered size code,
  and the form declares that code in `sizes`. A selector-less form obtains its
  size domain from `sizes`. A selected suffix names one registered
  `<size-kind-name>` and uses a field expression whose marker names exactly one
  `fields` entry with type
  `size.<size-kind-name>`. The form does not declare `sizes`. Instantiation
  selects among the codes and their registered suffixes owned by that size
  kind, in registry order.
- An owning registered mnemonic ending in the literal `cc` has exactly one
  encoded operand named `cc`, of type `condition`, whose `field` is declared in
  `bits`. That terminal `cc` is the condition-selector placeholder:
  instantiation replaces it with a primary condition name or alias whose value
  is admitted by the form's field constraints.
- `/order` followed by a field expression names exactly one encoded operand
  named `order`, of type `memory_order`, with that field marker. Its
  concrete selector is the enum name admitted for the encoded value and by the
  form's constraints. The `/order` selector follows a selected size suffix.
- Condition and order operands are represented by the instruction head.
  Operand-group nodes are excluded from `EncodingOperand` correspondence. Each
  remaining displayed non-group `<operand>` corresponds one-for-one, in YAML
  order, with one `EncodingOperand`. A field-bearing operand uses an `<operand-reference>`
  followed by a field expression with that exact marker. A fieldless operand
  uses its corresponding presentation from the next rule. Every displayed
  field-bearing encoded operand carries its field binding, and the displayed
  order is the declared operand order. A fieldless `EncodingOperand` may be
  undisplayed only when that form contains an operand-group node.
- A field-bearing non-EA operand uses a bare reference naming its registered
  operand type. A field-bearing operand of type `EA` uses the angle-bracket
  reference `<ea>`, whose concrete spelling is selected from `ea.yaml`. A
  fieldless payload supplied after the primary encoding uses an angle-bracket
  reference naming its registered operand type. A fieldless `fixed_register`
  operand uses a bare reference with the architectural register spelling from
  its registry entry. A decimal literal is the fixed nonnegative value of its
  corresponding fieldless operand for that form. These correspondence rules
  determine operand presentation. Encoded field binding is expressed by
  `<field-expression>`.

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

Values are unique within each list and cannot overlap reserved values. Valid
and reserved values together cover the complete encoded domain; that domain
determines the width of `size.<SizeKind>`. Size-field markers belong to each
encoding form rather than to the reusable size kind.

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

## 10. `isa/abi/plt_conformance_vectors.yaml`

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
