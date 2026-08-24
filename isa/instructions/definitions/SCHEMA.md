# YAML Schema Contract

This file displays the complete Bedrock YAML schema accepted by
`isa/tools/defs_schema.py`, including nested records and discriminated
variants. `schema.lock` pins the SHA-256 digests of both files.

Changing an allowed field, required field, value type, enum, path rule, or
cross-field invariant is a schema change. Synchronize this contract, its tests,
and `schema.lock` with each deliberate schema change.

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

The operation-bundle records use these lexical reference types:

```text
stable-id            string matching [A-Za-z][A-Za-z0-9_.-]*
form-id              string matching [a-z][a-z0-9_]*\.[a-z0-9_.]+
public-instruction-token
                     string matching [A-Za-z][A-Za-z0-9]*
CPUID-flag-id        stable-id registered by cpuid_flags.yaml
execution-route-id   enum(atomics, bounds, cache, control_flow, core_control,
                          data_movement, ea_utility, fpu,
                          fpu_transcendental_approx, integer_alu,
                          integer_bitfield, integer_mul_div, integer_unary,
                          system_registers, tlb_and_context, vector)
selector-id          stable-id naming a size-kind registry entry
selector-value-id    stable-id naming one resolved code in that size kind
operand-profile-id   stable-id naming an operand-type registry entry
logical-operand-id   stable-id in the operation's logical-operand membership
operand-value-domain enum(integer, floating, vector, predicate)
condition-id         stable-id supplied by the semantic-condition owner
named-value-id       stable-id supplied by named_values.yaml
flag-effect-definition-id
                     stable-id supplied by flag_effect_definitions.yaml
event-id             string matching [A-Z][A-Z0-9_]* supplied by the event owner
diagram-kind-id      stable-id supplied by the diagram-generator registry
Sail-identifier      string matching [A-Za-z][A-Za-z0-9_]*
```

Lexical validity establishes identity syntax. The operation coordinator checks
the registry-backed references named in the operation section below.

## `operation.yaml`

Each operation uses this unversioned manifest. The manifest owns typed
cross-artifact contracts and the reader-facing index title and summary. The
summary supplies both the instruction-set index row and the entry's concise
`Operation` field. The required description artifact supplies the complete
explanation under `Detailed Semantics`, immediately before any registered
diagrams.
Executable effects remain in Sail, natural explanation remains in the required
description artifact, and each registered diagram source owns its example and
layout inputs.

```text
OperationDocument {
  operation: stable-id
  title: string
  summary: string
  public_instruction: PublicInstructionRef
  execution_route: execution-route-id
  privilege: enum(unprivileged, supervisor, any)
  repeat: OperationRepeatEligibility
  operands: list<LogicalOperandDefinition, unique id>
  cases: non-empty list<OperationCase, unique id>
  artifacts: OperationArtifacts
}

PublicInstructionRef {
  mnemonic: public-instruction-token
  aliases?: list<public-instruction-token, unique and excluding mnemonic>
  width_suffix_aliases?: boolean
}

OperationRepeatEligibility = {
  kind: enum(not_eligible, rep)
} | {
  kind: rep_and_repcc
  observed: OperationRepeatObservation
}

OperationRepeatObservation =
  { kind: computed }
  | { kind: enum(result, source), operand: logical-operand-id }

LogicalOperandDefinition {
  id: stable-id
  role: enum(source, destination, address, control_target,
             governing_predicate, count, bit_index, segment_selector,
             counter, implicit)
  access: enum(read, write, read_write, address)
  value_domain: operand-value-domain
  profiles: non-empty list<operand-profile-id, unique>
}

OperationCase {
  id: stable-id
  applies_to: FormApplicability
  additional_requirements: list<CPUID-flag-id, unique>
  predicate: PredicateContract
  flags: list<FlagBankContract, unique bank>
  events: list<EventContract, unique event/condition pair>
  sail_entry: Sail-identifier
  conversion?: ConversionSignature
}

ConversionSignature {
  source_domain: enum(integer, floating)
  source_formats: non-empty list<public-size-code, unique>
  destination_domain: enum(integer, floating)
  destination_formats: non-empty list<public-size-code, unique>
  integer_signedness?: enum(signed, unsigned)
  behavior: enum(exact, sign_extend, zero_extend, convert)
}

FormApplicability {
  forms: non-empty list<form-id, unique>
  selectors?: list<SelectorApplicability, unique domain>
  operand_profiles?: list<OperandProfileApplicability, unique operand>
}

SelectorApplicability {
  domain: selector-id
  values: non-empty list<selector-value-id, unique>
}

OperandProfileApplicability {
  operand: logical-operand-id
  profiles: non-empty list<operand-profile-id, unique>
}

PredicateContract =
  { kind: none }
  | { kind: annul_on_false, condition_operand: logical-operand-id }
  | { kind: produce_boolean, condition_operand: logical-operand-id,
      destination_operand: logical-operand-id }
  | { kind: test_temporary, condition_operand: logical-operand-id,
      observed: named-value-id }
  | { kind: counter_and_condition, counter_operand: logical-operand-id,
      condition_operand: logical-operand-id }

FlagBankContract {
  bank: enum(FLAGS, FFLAGS)
  completion: enum(complete_image, accrued_causes)
  effects: non-empty list<FlagEffect, unique flag>
}

FlagEffect {
  flag: a flag in the selected bank
  effect: enum(preserve, clear, set, write_expression,
               write_condition, accrue_source)
  reference?: flag-effect-definition-id
}

EventContract {
  event: event-id
  condition: condition-id
  cause?: cause-id in the selected event's cause space
}

OperationArtifacts {
  semantics: { path: relative-path ending in .sail, kind: sail }
  description: { path: relative-path ending in .tex, kind: tex }
             | { path: relative-path ending in .md or .markdown, kind: markdown }
  diagrams?: list<{
    id: stable-id,
    path: relative-path ending in .yaml,
    kind: diagram-kind-id,
    case?: OperationCase.id,
    caption: reader-visible-figure-caption,
    alt_text: nonvisual-equivalent
  }, unique id and path>
}
```

A diagram is an illustrative presentation artifact owned by its operation
bundle. Its optional case reference limits the view to one declared operation
case. `caption` labels the visible figure; `alt_text` supplies the independent
nonvisual equivalent used by site output. Neither field defines operation
semantics.

`vector-example` is the current registered diagram kind. Every source fixes a
16-byte, right-to-left view and uses one of `lane-map`, `width-map`,
`predicate-range`, `predicate-width`, `predicate-lane-map`, `scalar-bridge`,
`memory-lanes`, `reduction`, or `conversion-map`. Lane maps accept a boolean
`view.scalable`; the renderer
shows continuation beyond the finite view only when it is true. Width maps and
predicate ranges retain scalable continuation. Lane and width maps declare
explicit rows and complete explicit cells, exactly one `destination-after`
row, and only the arrows intended to be visible, with bounded source and target
row/cell references and unique result targets. An edge effect equals its target
cell's displayed classification. Result cells remain complete even when no
arrow is displayed, including preserved and zero cells. Lane-map and detailed
width-map row order is authored per figure and is not normalized by the
renderer. A `predicate` row may explicitly show predicate bits, and a closed
cell `appearance` may select
the old-value, source-value, zero, discarded-field, predicate-on,
predicate-off, or don't-care presentation used by the reviewed finite example.

The initial width-map form retains four explicit 32-bit cells per row. A
detailed width-map instead declares `container_bits` as 16, 32, or 64, covers
the complete fixed view with that derived number of containers, and partitions
each source and result container into explicit cells whose `bits` sum to the
container width. It also declares all 16 byte positions in one predicate row.
Its explicit connections identify source and result container/cell indices and
select either a transfer arrow or an expansion guide; no coordinates or
operation expressions occur in the source. Width-map results use `copy`,
`preserve`, `sign-fill`, or `zero`. Predicate ranges declare every visible W
position as an explicit `set` or `clear` cell.

`predicate-width` is limited to the reviewed fixed 16-to-8 packing and 8-to-16
unpacking examples. It declares source and result element widths, a complete
result write, and one contiguous mapping. Mapping bounds use only zero,
`source-lanes`, or `destination-lanes`: packing maps all source positions to
one destination half, while unpacking maps one source half to all destination
positions. The renderer derives the eight displayed transfers and clears every
other result bit. It accepts no operation selector, coordinate, TikZ, or
runtime expression. These sources are finite illustrations rather than
semantic expressions.

The stateful `predicate-range` form adds exactly the `remaining` and `offset`
states, their displayed before/after values and endpoint anchors, and one
explicit half-open W-lane range. Its eight complete 16-bit predicate groups
must match that range. The original count/result form remains the finite PHEAD
example. Both forms are scalable and derive their layout without coordinates.

`predicate-lane-map` is limited to the reviewed W-width finite examples. It
authors two or three rows in their displayed order, with exactly eight
complete 16-bit predicate or vector groups per row. Predicate groups explicitly
classify their significant value and nonsignificant bit; the one complete
result row explicitly classifies copied or cleared significant values and
clears every nonsignificant bit. Its ordered edge list is the complete visible
arrow set: predicate sources use transfer arrows, vector sources use control
arrows, and every copied result value has exactly one transfer. The renderer
does not reorder rows or infer arrows. The source accepts no operation
selector, coordinate, TikZ, or runtime expression.

`scalar-bridge` authors one complete vector row, a unique set of scalar source,
index, or destination roles, and only the visible transfer and index-control
connections. An insertion and an extraction mark exactly one vector cell with
the closed `selected-source` appearance; their single transfer and single index
control connection address that same cell. An extraction transfers that cell
to its scalar destination. A broadcast from one scalar source marks every
destination cell with the ordinary source appearance and transfers to every
cell exactly once. The renderer preserves the authored endpoint order and does
not infer connections.

`memory-lanes` authors complete address, memory, result, and byte-predicate
rows for one element width. Every active memory lane has one corresponding
address-control connection and one memory-to-result transfer. Its address,
memory, result, and significant predicate positions classify the same active
lane set. Inactive address and memory lanes use the closed `no-access`
appearance, and their result lanes preserve the previous destination value.
`reduction` authors a complete source and byte-predicate view, increasing
selected lane indices, an ordered fold term list whose tail equals those source
values, and a scalar result. Source and predicate classifications select the
same lanes; predicate significance is derived from the element width.

`conversion-map` is a separate finite widening/narrowing variant. It authors
complete 32- or 64-bit containers for distinct 16-, 32-, or 64-bit source and
result widths, a complete byte-predicate row, and the visible conversion
connections. Every source container contains one copied field of the declared
source element width. Each active result container contains one copied field of
the declared result element width, and the significant predicate positions
select exactly those active containers. The connections target every copied
result field exactly once. Its renderer reuses the reviewed container
presentation grammar; the source remains explicit and contains no operation
selector, expression evaluator, coordinate, or TikZ fragment.

The sibling `encodings.yaml` owns the operation's complete form membership.
Each `FormApplicability.forms` list owns the relation between one case and the
encoding forms to which it applies. The coordinator validates those references
against the encoding-owned membership and derives the canonical operation form
list from `encodings.yaml`.

`FLAGS` uses `complete_image`; `FFLAGS` uses `accrued_causes`. A complete-image
contract permits `preserve`, `clear`, `set`, `write_expression`, and
`write_condition`. An accrued-causes contract permits `preserve` and
`accrue_source`. Each reference-bearing effect carries exactly one `reference`;
constant and preserve effects carry none. The referenced registry definition
must have the matching expression, condition, or accrued-source kind. Predicate
and repeat operand references name declared logical operands and are present in
every form to which their contract applies. `computed` is a complete
payload-free repeat observation. A temporary predicate observation names a
registered named value.

The source list may omit architectural flags. The strict operation decoder
inserts `preserve` for each omission and orders canonical effects by
`FLAG_BANK_FLAGS`: `Z, N, C, V` for FLAGS and `NV, DZ, OF, UF, NX` for FFLAGS.
Every canonical `OperationFlagBankContract` is therefore a TotalMap. Renderers
and downstream consumers read that map directly.

The loader requires `operation.yaml` for every indexed operation directory.

Candidate admission resolves every artifact inside the operation directory,
checks that it is a regular file of the declared kind, derives operation form
membership from `encodings.yaml`, and resolves every case form reference
against that membership. For each form it enumerates legal resolved selector
values from the size registry and encoding constraints plus the form's exact
operand profiles. Cases partition those tuples: coverage is total and
exclusive, and every case is reachable. Applicability is determined from exact
form references, selector domain/value references, and operand-profile
references.

The canonical artifact projection records the resolved bundle root and
`operation.yaml` path together with each relative artifact reference. A
consumer locates semantics, description, and diagrams from this provenance;
operation ID, public mnemonic, and directory spelling remain outside path
resolution.

Operation ID, directory basename, and public mnemonic are independent. Public
instruction tokens have one global operation owner across canonical mnemonics
and aliases. Each encoding template begins with a token declared by its
operation; aliases participate in the same ownership and form-membership check.
The Decode IR mnemonic inventory contains the tokens used by encoding forms.
An owned alias may feed assembler or toolchain projection without adding a
duplicate encoding form. Public instruction aliases are complete mnemonic
tokens; assembly suffix aliases remain part of the suffix/toolchain contract.

The CPUID flag registry owns each stable ID, public token, and architectural
location independently of extension identity. Each extension owns only its
local requirements. The coordinator inherits parent requirements, rejects a
local requirement already inherited from an ancestor, validates case-specific
IDs against the registry, rejects case entries already inherited by the
operation, then joins the two sets.

Event IDs and event-specific cause spaces resolve through
`architecture_tables.yaml`; a cause is valid only in the selected event's
cause space, and events without a cause space reject one. Event conditions use
the IDs in `semantic_conditions.yaml`; the same registry owns their
reader-facing conditional prose. A `destination_overlap` condition additionally
requires every selected encoding form to declare an `illegal_instruction`
`destination_overlap` relation. The renderer publishes the architectural event
and optional cause plus registry-owned condition text, without publishing the
condition ID. Temporary predicate observations use the named-value set.
Reference-bearing flag effects resolve through `flag_effect_definitions.yaml`,
which owns their kind and reader text. CPUID flags, execution routes,
operand value domains, operand profiles, diagram kinds, and public instruction
tokens each retain their own owner and validation boundary.
Diagram kinds resolve through the supplied diagram-generator registry; the
current registry contains `vector-example` for the strict finite-view variants
defined above. The coordinator validates Sail entry lexical form.

`CanonicalOperation` carries the exact `forms` and `logical_operand_ids`
memberships derived from the encoding forms. Every operation carries the full
`operands` tuple, including an empty tuple for an operation with no operands,
and its IDs equal that membership. Operations carry a registered execution route and
privilege in FormIR; its `operation_cases` predicate mode directs case-contract
readers to OperationIR. FormIR leaves the deprecated class, family, and
free-form annotations empty. Every case exposes the resolved CPUID conjunction
and carries every typed contract above. Each FormIR preserves the exact covering
case partition as typed availability rules with encoded selector values,
operand profiles, and resolved CPUID flag IDs.

## 3. `encodings.yaml`

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
  ea_role: enum(value, address, control_target) when type is an effective_address
  ea_width: enum(operation_size, B, W, L, Q) when type is an effective_address
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
Logical operand access records how the operation uses a value, while encoding
operand access records how a form transports that value. These accesses match
directly except for two closed transport pairs. A logical operand with role
`address`, access `address`, and exactly the profiles `EA` and `Rn` accepts `EA`
with encoding access `address` and `ea_role: address`, or `Rn` with encoding
access `read`. A logical operand with role `destination`, access `read_write`,
value domain `vector`, and exactly the profiles `Vn` and `VEA` accepts `Vn`
with encoding access `read_write` and no EA role, or `VEA` with encoding access
`write` or `read_write` and `ea_role: value`. Every other profile or access
combination follows exact access equality.
Every effective-address operand declares both `ea_role` and `ea_width`. `address` role uses
`address` access, `control_target` role uses `read` access, and `value` role
uses `read`, `write`, or `read_write` access. Each operand or field type names
one entry in the merged operand/size field-type registry, and its marker count
in `bits` equals that type's encoded width. An encoded size selector uses an
explicit `size.<SizeKind>` type; its size choices are derived from that kind,
so the form does not also declare `sizes`. Selector-less and fixed-size forms
continue to declare `sizes` directly. `operation_size` requires a resulting
size domain; fixed widths define extended-descriptor index scale and pre/post-update amount
directly. Reserved size-kind values must be excluded by an `allow` constraint
on the selector field. Field-marker bits need not be contiguous.
Every pair of writable field operands of the same register type that can
designate the same architectural register has exactly one
`destination_overlap` entry. EA operands do not participate because compact EA
has no register-direct form.

### Assembly-template language

The following BNF and correspondence rules define canonical template values
for `EncodingForm.syntax`. In the BNF, quoted strings
are literal text, angle-bracketed names are nonterminals, `|` separates
alternatives, and all repetition is expressed by recursion.

```text
<encoding-form-syntax> ::= <instruction-template>
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
            | <vector-address>

<operand-reference> ::= <operand-name>
                      | "<" <operand-name> ">"

<field-expression> ::= "(" <field-marker> ")"

<operand-group> ::= "(" <operand-reference> ")"
                  | "{" " " <operand-reference> "..." " " "}"

<vector-address> ::= "[" <vector-address-expression> "]"
<vector-address-expression> ::= an ordered sequence of operand references,
                                decimal scale literals or "<scale>", nested
                                lane-selection brackets, "+", and "*"

<decimal-literal> ::= <decimal-digit>
                    | <decimal-digit> <decimal-literal>
<decimal-digit> ::= "0" | "1" | "2" | "3" | "4"
                  | "5" | "6" | "7" | "8" | "9"
```

The grammar uses lexical classes owned by the existing definitions:

- `<mnemonic-name>` has the `public-instruction-token` lexical form. Its owning
  canonical public mnemonic/full-alias relation is determined by the
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
  concrete effective-address spelling owned by
  `isa/addressing/effective_address/definition.yaml`.

All terminals are case-sensitive. Canonical templates use one explicit space
terminal between a head and its first operand, and comma plus one space between
operands.

The following correspondence rules restrict the BNF to well-formed canonical
templates:

- The base `<mnemonic-name>` of an `EncodingForm.syntax` is the operation's
  canonical public mnemonic or an owned full-mnemonic alias. When
  `width_suffix_aliases` is true, the toolchain additionally accepts the
  established `.H`, `.S`, and `.D` width aliases for that operation's eligible
  width forms; canonical output remains the registered public size code.
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
  Operand-group nodes are excluded from `EncodingOperand` correspondence.
  Operand references inside a vector address are flattened in their displayed
  order. Each remaining displayed operand reference corresponds one-for-one,
  in YAML order, with one `EncodingOperand`. A field-bearing operand uses an `<operand-reference>`
  followed by a field expression with that exact marker. A fieldless operand
  uses its corresponding presentation from the next rule. Every displayed
  field-bearing encoded operand carries its field binding, and the displayed
  order is the declared operand order. A fieldless `EncodingOperand` may be
  undisplayed only when that form contains an operand-group node.
- A field-bearing non-EA operand uses a bare reference naming its registered
  operand type. A field-bearing operand of type `EA` uses the angle-bracket
  reference `<ea>`, whose concrete spelling is selected from
  `isa/addressing/effective_address/definition.yaml`. A
  fieldless payload supplied after the primary encoding uses an angle-bracket
  reference naming either its registered operand type or its operand name when
  the syntax needs a semantic label such as a displacement. A fieldless `fixed_register`
  operand uses a bare reference with the architectural register spelling from
  its registry entry. A decimal literal is the fixed nonnegative value of its
  corresponding fieldless operand for that form. These correspondence rules
  determine operand presentation. Encoded field binding is expressed by
  `<field-expression>`.

## 4. `instructions.yaml`

```text
InstructionSetIndex {
  title: string
  include: non-empty list<relative-path, unique>
  introduction?: relative-path ending in .tex
}
```

The `include` sequence is also the document order.

## 5. CPUID flag and extension documents

`cpuid_flags.yaml`:

```text
CpuidFlagRegistry {
  cpuid_flags: list<CpuidFlag>
}

CpuidFlag {
  id: CPUID-flag-id
  token: string matching [A-Za-z][A-Za-z0-9]*
  location: CpuidFlagLocation
}

CpuidFlagLocation {
  class: int[0..]
  leaf: int[0..]
  index: int[0..]
  bit: int[0..63]
}
```

Flag IDs, public tokens, and complete locations are independently unique.

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
  required_cpuid_flags: non-empty list<CPUID-flag-id, unique>
}
```

An extension lists only local requirements. Requirements from every ancestor
extension are inherited in order and conjoined with local requirements.

## 6. `operands.yaml`

```text
OperandRegistry {
  operand_types: map<string, OperandType>
}

OperandTypeCommon {
  kind: OperandKind
  bit_width: int[0..]
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
  bit_width: int[0..]
  register_group: string
}

kind: fixed_register {
  kind: fixed_register
  bit_width: int[0..]
  register: string
}

kind: effective_address {
  kind: effective_address
  bit_width: int[0..]
  encoding_ref: string
  profile: enum(ea, fea, vea)
}

kind: enum {
  kind: enum
  bit_width: int[0..]
  exactly-one(
    values: list<OperandEnumValue>,
    values_ref: string
  )
  reserved_values?: list<OperandEnumValue>
  result_bits_format?: string
}

kind: ea_immediate {
  kind: ea_immediate
  bit_width: int[0..]
  encoding_ref: string
}

kind: bitmap {
  kind: bitmap
  bit_width: int[0..]
  bits: list<OperandBit>
}

kind: immediate | relative_immediate {
  kind: enum(immediate, relative_immediate)
  bit_width: int[0..]
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
  bit: int[0..bit_width-1]
  name: string
}
```

Enum/reserved values and names are unique within their lists and combined enum
numeric/string values do not overlap. Bitmap bit numbers and names are unique.

## 7. `sizes.yaml`

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

## 8. `registers.yaml`

```text
RegisterRegistry {
  registers: map<string, RegisterGroup>
}

RegisterGroup {
  entries: non-empty list<RegisterEntry>
}

RegisterEntry {
  name: string
  width: int[1..] | enum(VLEN, VLEN_bytes)
  encoding?: int[0..]
  role?: string
  description?: string
}
```

The symbolic widths are used only by scalable-vector register groups:
\texttt{VLEN} is the implementation-selected vector-register width in bits,
and \texttt{VLEN\_bytes} is the number of predicate bits (one per vector byte).

Names and present encodings are unique within a register group.

## 9. `conditions.yaml`

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

## 10. `semantic_conditions.yaml`

```text
SemanticConditionRegistry {
  conditions: non-empty list<SemanticConditionDefinition, unique id>
}

SemanticConditionDefinition {
  id: stable-id
  reader_text: string
}
```

An operation event stores the stable condition ID. Document renderers resolve
that reference through this registry and publish `reader_text`, keeping the
internal ID out of reader-facing event descriptions.

## 11. `named_values.yaml`

```text
NamedValueRegistry {
  values: non-empty list<NamedValueDefinition, unique id>
}

NamedValueDefinition {
  id: stable-id
  kind: enum(condition_code_image)
  reader_term: string
}
```

A temporary predicate observation stores a stable named-value ID. Each current
value is an operation-defined condition-code image used to evaluate a branch
condition without writing architectural FLAGS. Reader-facing consumers use the
registry-owned term instead of publishing the internal ID.

## 12. `flag_effect_definitions.yaml`

```text
FlagEffectDefinitionRegistry {
  definitions: non-empty list<FlagEffectDefinition, unique id>
}

FlagEffectDefinition {
  id: stable-id
  kind: enum(expression, condition, accrued_source)
  reader_text: string
}
```

Reference-bearing operation flag effects resolve their internal IDs through
this registry. `write_expression`, `write_condition`, and `accrue_source`
require definitions of kind `expression`, `condition`, and `accrued_source`,
respectively. Document renderers publish only the registry-owned reader text.

## 13. `isa/addressing/effective_address/definition.yaml`

```text
EaRegistry {
  payloads: map<string, EaPayload>
  compact: CompactEaSection
  ext1: Ext1EaSection
  ext2: Ext2EaSection
}

EaPayload {
  kind: string
  bit_width: int[1..]
  signed: bool
  format?: enum(binary32, binary64)
}

CompactEaSection {
  field_width: int[1..]
  profiles: map containing exactly ea, fea, and vea CompactEaProfile values
  forms: list<CompactEaForm>
}

CompactEaProfile {
  operand_type: string
  overrides: list<CompactEaOverride, unique exact pattern>
  immediate_conversion?: enum(ieee754)
  lane_model?: enum(contiguous)
  base_update?: enum(vlen_bytes)
  index_update?: enum(element_count_before_scale)
  predicate_affects_update?: bool
  scatter_gather?: enum(separate_instructions)
}

CompactEaOverride = {
  pattern: exact 0/1 BitPattern of CompactEaSection.field_width bits
  reserved: true
} | CompactEaForm with an exact 0/1 pattern

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

Ext1EaSection {
  kind: string
  forms: list<Ext1EaForm>
}

Ext1EaForm {
  name: string
  pattern: list containing exactly one BitPattern of exactly 8 bits
  syntax: string
  fields?: map<one lowercase marker, EaField>
  segment?: string
  base?: string
  update?: EaUpdate
}

Ext2EaSection {
  kind: string
  forms: list<Ext2EaForm>
}

Ext2EaForm {
  name: string
  pattern: list containing exactly two BitPatterns of exactly 8 bits
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

The `EA`/`ea`, `FEA`/`fea`, and `VEA`/`vea` operand-type/profile pairs are
fixed. Scalar EA is the unchanged `compact.forms` baseline and has no
overrides; FEA and VEA record only exact-value differences from that baseline.
Only `float_immediate` payloads carry `format`, and every such payload carries
it.

Every compact form with `kind: escape` names exactly one declared descriptor
family in `descriptor`; non-escape compact forms do not name a descriptor
family. The compact form therefore fixes the descriptor length before its
descriptor bytes are parsed.

Form names are unique per section. Every pattern marker has exactly one field
declaration and vice versa. Compact `payload` values reference a declared
`payloads` key.

## 14. `isa/interfaces/abi/plt_conformance_vectors.yaml`

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
  opcode_space_bytes: list<int[0..255]>
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

## 15. `isa/memory/ordering/formal/validation.yaml`

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
- indexes cover every definition exactly once, and public mnemonics are
  globally unique;
- candidate artifact references stay inside the bundle, have the declared file
  kind, and resolve to regular files;
- form membership is derived from `encodings.yaml`, every case form
  reference resolves within that membership, logical operands cover referenced
  form operands and profiles, and typed cases form a total, exclusive,
  reachable partition of legal form/selector/profile tuples;
- operations carry full logical operand definitions;
- operation ID, directory name, and public mnemonic remain separate identities;
  every public mnemonic and alias has one global operation owner, and every
  encoding template uses a token owned by its operation;
- CPUID, semantic-condition, named-value, event,
  execution-route, operand-value-domain, operand-profile, and diagram-kind
  references resolve through their distinct owners;
- operand and size names are registered, encoding marker widths equal their
  primitive widths, and EA write destinations reclaim immediate encodings;
- CPUID flag IDs, public tokens, and `(class, leaf, index, bit)` locations are
  unique, extension references resolve through that registry, and no local
  requirement duplicates an inherited requirement;
- encoding IDs are globally stable, class names and bit widths match the fixed
  grammar in `isa/tools/encoding_architecture.py`, and concrete opcode claims
  do not overlap.
