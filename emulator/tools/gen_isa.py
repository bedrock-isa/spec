#!/usr/bin/env python3
"""Generate emulator decode descriptors from this repository's ISA definitions."""

from __future__ import annotations

import argparse
import hashlib
from itertools import product
from pathlib import Path
import re
import sys
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required to generate the emulator ISA table") from exc


EMULATOR_ROOT = Path(__file__).resolve().parent.parent
REPOSITORY_ROOT = EMULATOR_ROOT.parent


CLASS_ORDER = ["extrashort", "short", "medium", "long", "extralong", "xxlong"]

RUST_ENCODING_CLASSES = {
    "extrashort": "ExtraShort",
    "short": "Short",
    "medium": "Medium",
    "long": "Long",
    "extralong": "ExtraLong",
    "xxlong": "Xxlong",
}

PREDICATE_VALUES = {
    "immediate": set(range(0x5B, 0x5F)),
}

FIELDLESS_OPERAND_WIDTHS = {
    "CS": 0,
    "SP": 0,
    "imm": 0,
    "imm8": 1,
    "imm8s": 1,
    "imm16": 2,
    "imm16s": 2,
    "imm32": 4,
    "imm32s": 4,
    "imm64": 8,
    "fconst_id": 2,
}


def validated_output_path(output: Path) -> Path:
    """Resolve output and reject generated Rust beneath repository src trees."""

    resolved = output.resolve()
    try:
        relative = resolved.relative_to(REPOSITORY_ROOT.resolve())
    except ValueError:
        return resolved
    if "src" in relative.parts[:-1]:
        raise ValueError(
            f"generated Rust output must not be under a repository src directory: {resolved}"
        )
    return resolved


def rust_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_range(value: Any) -> tuple[int, int]:
    if isinstance(value, int):
        return value, value
    text = str(value)
    if ".." in text:
        lo, hi = text.split("..", 1)
        return int(lo, 0), int(hi, 0)
    parsed = int(text, 0)
    return parsed, parsed


def pattern_mask_value(pattern: str) -> tuple[int, int]:
    mask = 0
    value = 0
    for char in pattern:
        mask <<= 1
        value <<= 1
        if char == "0":
            mask |= 1
        elif char == "1":
            mask |= 1
            value |= 1
    return mask, value


def value_set_cubes(values: set[int], width: int) -> list[tuple[int, int]]:
    """Return disjoint prefix cubes covering exactly values within width bits."""

    limit = 1 << width
    if any(value < 0 or value >= limit for value in values):
        raise ValueError(f"field value outside {width}-bit domain")

    def visit(prefix: int, consumed: int) -> list[tuple[int, int]]:
        remaining = width - consumed
        start = prefix << remaining
        stop = (prefix + 1) << remaining
        count = sum(1 for value in values if start <= value < stop)
        if count == 0:
            return []
        if count == stop - start:
            mask = ((1 << consumed) - 1) << remaining if consumed else 0
            return [(mask, start)]
        return visit(prefix << 1, consumed + 1) + visit((prefix << 1) | 1, consumed + 1)

    return visit(0, 0)


def translate_field_cube(
    pattern: str, symbol: str, field_mask: int, field_value: int
) -> tuple[int, int]:
    positions = [len(pattern) - index - 1 for index, char in enumerate(pattern) if char == symbol]
    width = len(positions)
    payload_mask = 0
    payload_value = 0
    for occurrence, payload_bit in enumerate(positions):
        field_bit = width - occurrence - 1
        if field_mask & (1 << field_bit):
            payload_mask |= 1 << payload_bit
            if field_value & (1 << field_bit):
                payload_value |= 1 << payload_bit
    return payload_mask, payload_value


def accepted_cubes(
    entry: dict[str, Any], pattern: str, base_mask: int, base_value: int, label: int
) -> list[tuple[int, int, int]]:
    """Compile a form pattern and its constraints into disjoint payload cubes."""

    fields = entry.get("fields") or {}
    allowed_by_field: dict[str, set[int]] = {}
    for constraint in entry.get("constraints") or []:
        symbol = constraint.get("field")
        if constraint.get("destination"):
            symbol = next(
                (
                    name
                    for name in ("d", "e")
                    if name in fields and int(fields[name]["width"]) == 7
                ),
                None,
            )
        if symbol is None or symbol not in fields:
            raise ValueError(f"{entry['id']}: constraint has no resolvable field")
        symbol = str(symbol)
        width = int(fields[symbol]["width"])
        allowed = allowed_by_field.setdefault(symbol, set(range(1 << width)))
        if "allow" in constraint:
            permitted: set[int] = set()
            for item in constraint["allow"]:
                lo, hi = parse_range(item)
                permitted.update(range(lo, hi + 1))
            allowed.intersection_update(permitted)
        else:
            predicate = str(constraint["exclude"])
            try:
                excluded = PREDICATE_VALUES[predicate]
            except KeyError as exc:
                raise ValueError(f"unknown exclude predicate {predicate!r}") from exc
            allowed.difference_update(excluded)

    covers: list[list[tuple[int, int]]] = []
    for symbol, values in sorted(allowed_by_field.items()):
        width = int(fields[symbol]["width"])
        covers.append(
            [
                translate_field_cube(pattern, symbol, field_mask, field_value)
                for field_mask, field_value in value_set_cubes(values, width)
            ]
        )

    if not covers:
        return [(base_mask, base_value, label)]
    return [
        (
            base_mask | sum((mask for mask, _ in choices), 0),
            base_value | sum((value for _, value in choices), 0),
            label,
        )
        for choices in product(*covers)
    ]


def fill_direct_table(bits: int, cubes: list[tuple[int, int, int]]) -> list[int]:
    table = [0] * (1 << bits)
    for mask, value, label in cubes:
        free_bits = [bit for bit in range(bits) if not mask & (1 << bit)]
        for assignment in range(1 << len(free_bits)):
            payload = value
            for index, bit in enumerate(free_bits):
                if assignment & (1 << index):
                    payload |= 1 << bit
            encoded = label + 1
            if table[payload] not in (0, encoded):
                raise ValueError(f"direct decode collision at payload 0x{payload:x}")
            table[payload] = encoded
    return table


def rust_u16_array(values: list[int], indent: str = "    ") -> list[str]:
    return [
        indent + ", ".join(str(value) for value in values[index : index + 32]) + ","
        for index in range(0, len(values), 32)
    ]


def render_direct_table(name: str, bits: int, cubes: list[tuple[int, int, int]]) -> list[str]:
    values = fill_direct_table(bits, cubes)
    if bits <= 14:
        return [
            "#[rustfmt::skip]",
            f"static {name}_LOOKUP: [u16; {len(values)}] = [",
            *rust_u16_array(values),
            "];",
            "",
        ]

    page_bits = 8
    page_size = 1 << page_bits
    pages: list[tuple[int, ...]] = []
    page_ids: dict[tuple[int, ...], int] = {}
    page_index: list[int] = []
    for offset in range(0, len(values), page_size):
        page = tuple(values[offset : offset + page_size])
        if page not in page_ids:
            page_ids[page] = len(pages)
            pages.append(page)
        page_index.append(page_ids[page])
    rows = ["#[rustfmt::skip]", f"static {name}_PAGE_INDEX: [u16; {len(page_index)}] = ["]
    rows.extend(rust_u16_array(page_index))
    rows.extend(["];", "#[rustfmt::skip]", f"static {name}_PAGES: [[u16; {page_size}]; {len(pages)}] = ["])
    for page in pages:
        rows.append("    [")
        rows.extend(rust_u16_array(list(page), "        "))
        rows.append("    ],")
    rows.extend(["];", ""])
    return rows


def build_hierarchical_lookup(
    cubes: list[tuple[int, int, int]], bits: int, stride: int = 6
) -> tuple[int, list[tuple[int, int, tuple[int, ...]]], int]:
    """Build a reduced high-to-low multi-bit lookup hierarchy."""

    nodes: list[tuple[int, int, tuple[int, ...]]] = []
    node_ids: dict[tuple[int, int, tuple[int, ...]], int] = {}
    memo: dict[tuple[int, tuple[tuple[int, int, int], ...]], int] = {}

    def leaf(label: int) -> int:
        return 0x80000000 | (label + 1)

    def reduce_cubes(items: tuple[tuple[int, int, int], ...]) -> tuple[tuple[int, int, int], ...]:
        unique = sorted(set((mask, value & mask, label) for mask, value, label in items))
        kept: list[tuple[int, int, int]] = []
        for candidate in unique:
            mask, value, label = candidate
            if any(
                other_label == label
                and other_mask & mask == other_mask
                and value & other_mask == other_value
                for other_mask, other_value, other_label in unique
                if (other_mask, other_value, other_label) != candidate
            ):
                continue
            kept.append(candidate)
        return tuple(kept)

    def visit(items: tuple[tuple[int, int, int], ...], high: int) -> int:
        items = reduce_cubes(items)
        if not items:
            return 0
        memo_key = (high, items)
        if memo_key in memo:
            return memo[memo_key]
        wildcards = {label for mask, _, label in items if mask == 0}
        if wildcards:
            labels = {label for _, _, label in items}
            if len(labels) != 1:
                raise ValueError(f"hierarchical lookup contains overlapping labels {sorted(labels)}")
            edge = leaf(next(iter(labels)))
            memo[memo_key] = edge
            return edge
        if high == 0:
            raise ValueError("hierarchical lookup exhausted payload bits before reaching a leaf")

        width = min(stride, high)
        shift = high - width
        slot_count = 1 << width
        chunk_mask = (slot_count - 1) << shift
        branches: list[list[tuple[int, int, int]]] = [[] for _ in range(slot_count)]
        for mask, value, label in items:
            constrained = mask & chunk_mask
            for slot in range(slot_count):
                slot_value = slot << shift
                if (slot_value ^ value) & constrained == 0:
                    branches[slot].append((mask & ~chunk_mask, value & ~chunk_mask, label))
        children = tuple(visit(tuple(branch), shift) for branch in branches)
        if len(set(children)) == 1:
            edge = children[0]
            memo[memo_key] = edge
            return edge
        node = (shift, width, children)
        node_index = node_ids.get(node)
        if node_index is None:
            node_index = len(nodes)
            nodes.append(node)
            node_ids[node] = node_index
        edge = node_index + 1
        memo[memo_key] = edge
        return edge

    root = visit(tuple(cubes), bits)

    depth_memo: dict[int, int] = {}

    def depth(edge: int) -> int:
        if edge == 0 or edge & 0x80000000:
            return 0
        if edge not in depth_memo:
            depth_memo[edge] = 1 + max(depth(child) for child in nodes[edge - 1][2])
        return depth_memo[edge]

    return root, nodes, depth(root)


def render_hierarchical_lookup(
    name: str, bits: int, cubes: list[tuple[int, int, int]]
) -> list[str]:
    root, nodes, max_depth = build_hierarchical_lookup(cubes, bits)
    offsets: list[int] = []
    edges: list[int] = []
    for _shift, _width, children in nodes:
        offsets.append(len(edges))
        edges.extend(children)
    rows = [
        f"const {name}_ROOT: u32 = 0x{root:08x};",
        f"pub const {name}_LOOKUP_MAX_DEPTH: u8 = {max_depth};",
        "#[rustfmt::skip]",
        f"static {name}_TABLES: [DecodeTable; {len(nodes)}] = [",
    ]
    rows.extend(
        f"    DecodeTable {{ shift: {shift}, mask: 0x{(1 << width) - 1:02x}, offset: {offset} }},"
        for (shift, width, _children), offset in zip(nodes, offsets)
    )
    rows.extend([
        "];",
        "#[rustfmt::skip]",
        f"static {name}_EDGES: [u32; {len(edges)}] = [",
    ])
    rows.extend(
        "    " + ", ".join(f"0x{edge:08x}" for edge in edges[index : index + 16]) + ","
        for index in range(0, len(edges), 16)
    )
    rows.extend([
        "];",
        "",
    ])
    return rows


def mnemonic(text: str) -> str:
    head = text.strip().split()[0]
    head = head.split("(", 1)[0].split("/", 1)[0].split(".", 1)[0]
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", head):
        raise ValueError(f"cannot derive mnemonic from {text!r}")
    return head.upper()


def fixed_operand_bytes(entry_id: str, operands: list[dict[str, Any]]) -> int:
    total = 0
    for operand in operands:
        if operand.get("field") is not None:
            continue
        operand_type = str(operand.get("type"))
        try:
            total += FIELDLESS_OPERAND_WIDTHS[operand_type]
        except KeyError as error:
            raise ValueError(
                f"{entry_id}: fieldless operand {operand.get('name')!r} "
                f"has unknown payload width for type {operand_type!r}"
            ) from error
    if total > 0xFF:
        raise ValueError(f"{entry_id}: fixed operand payload exceeds u8")
    return total


def rust_variant(value: str) -> str:
    parts = [part for part in re.split(r"[^A-Za-z0-9]+", value) if part]
    if not parts:
        raise ValueError(f"cannot create Rust identifier from {value!r}")
    rendered = "".join(("N" + part if part[0].isdigit() else part[0].upper() + part[1:].lower()) for part in parts)
    if rendered[0].isdigit():
        rendered = "N" + rendered
    return rendered


def digest_inputs(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(str(path).encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def load_definitions(isa_design: Path) -> tuple[dict[str, dict[str, Any]], list[Path]]:
    root = isa_design / "isa" / "instructions" / "definitions"
    definitions: dict[str, dict[str, Any]] = {}
    paths = sorted(root.glob("**/instructions/*/instruction.yaml"))
    for path in paths:
        definition = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(definition, dict) or "mnemonic" not in definition:
            continue
        relative = path.relative_to(root)
        if relative.parts[0] == "instructions":
            instruction_set = "base"
        elif relative.parts[0] == "extensions" and relative.parts[1] == "vector":
            instruction_set = "vector"
        elif "transcendental_approx" in relative.parts:
            instruction_set = "fpu_transcendental"
        else:
            instruction_set = "fpu"
        item = dict(definition)
        item["instruction_set"] = instruction_set
        definitions[str(definition["mnemonic"]).upper()] = item
    return definitions, paths


def generated_attributes(
    definition: dict[str, Any],
    entry: dict[str, Any],
    operands: list[dict[str, Any]],
) -> str:
    attributes = definition.get("attributes") or {}
    repeat = definition.get("repeat") or {}
    repeat_contexts = set(repeat.get("contexts") or [])
    mnemonic_name = str(definition.get("mnemonic", "")).upper()
    flags = definition.get("flag_effects")
    if mnemonic_name == "REPCC":
        flags_mode = "Body"
    elif isinstance(flags, dict):
        flags_mode = "Writes"
    elif flags is None:
        flags_mode = "Unchanged"
    else:
        flags_mode = "OperationDefined"
    return (
        "GeneratedAttributes { "
        f"instruction_set: InstructionSet::{rust_variant(str(definition.get('instruction_set', 'unknown')))}, "
        f"privileged: {str(attributes.get('privilege') == 'supervisor').lower()}, "
        f"repeat_rep: {str('REP' in repeat_contexts).lower()}, "
        f"repeat_repcc: {str('REPcc' in repeat_contexts).lower()}, "
        f"repeat_observed: {generated_repeat_observation(definition, entry, operands)}, "
        f"flags: FlagsEffect::{flags_mode} "
        "}"
    )


def generated_repeat_observation(
    definition: dict[str, Any],
    entry: dict[str, Any],
    operands: list[dict[str, Any]],
) -> str:
    repeat = definition.get("repeat") or {}
    repeat_contexts = set(repeat.get("contexts") or [])
    observed = repeat.get("observed")
    if observed is None:
        if "REPcc" in repeat_contexts:
            raise ValueError(
                f"{entry['id']}: REPcc-capable form has no repeat.observed metadata"
            )
        return "None"
    if "REPcc" not in repeat_contexts:
        raise ValueError(
            f"{entry['id']}: repeat.observed is only valid for REPcc-capable forms"
        )
    if not isinstance(observed, dict):
        raise ValueError(f"{entry['id']}: repeat.observed must be a mapping")

    kind = str(observed.get("kind", ""))
    if kind == "computed":
        if observed.get("operand") is not None:
            raise ValueError(
                f"{entry['id']}: computed observation cannot name an operand"
            )
        return "Some(RepeatObservation::Computed)"
    if kind not in {"result", "source"}:
        raise ValueError(
            f"{entry['id']}: unknown repeat observation kind {kind!r}"
        )

    operand_name = observed.get("operand")
    if not isinstance(operand_name, str) or not operand_name:
        raise ValueError(
            f"{entry['id']}: {kind} observation requires an operand"
        )

    matches = [operand for operand in operands if operand.get("name") == operand_name]
    if not matches:
        raise ValueError(
            f"{entry['id']}: repeat observation names unknown operand {operand_name!r}"
        )
    if len(matches) != 1:
        raise ValueError(
            f"{entry['id']}: repeat observation operand {operand_name!r} is duplicated"
        )

    operand = matches[0]
    access = operand.get("access")
    valid_accesses = {"result": {"write", "read_write"}, "source": {"read", "read_write"}}
    if access not in valid_accesses[kind]:
        raise ValueError(
            f"{entry['id']}: {kind} observation operand {operand_name!r} "
            f"has incompatible access {access!r}"
        )

    operand_type = operand.get("type")
    locations = {
        "Rn": ("Rn", "rn"),
        "EA": ("EffectiveAddress", "ea7"),
        "SP": ("StackPointer", None),
        "SREG": ("SegmentRegister", "bits"),
        "CS": ("CodeSegment", None),
    }
    if operand_type not in locations:
        raise ValueError(
            f"{entry['id']}: repeat observation operand {operand_name!r} "
            f"has unsupported type {operand_type!r}"
        )
    location, expected_field_kind = locations[operand_type]

    field = operand.get("field")
    if field is None:
        if expected_field_kind is not None:
            raise ValueError(
                f"{entry['id']}: repeat observation operand {operand_name!r} "
                f"of type {operand_type!r} requires an encoded field"
            )
        field_expr = "None"
    else:
        if not isinstance(field, str) or len(field) != 1:
            raise ValueError(
                f"{entry['id']}: repeat observation operand {operand_name!r} "
                f"has invalid field symbol {field!r}"
            )
        if expected_field_kind is None:
            raise ValueError(
                f"{entry['id']}: fixed repeat observation operand {operand_name!r} "
                f"cannot have encoded field {field!r}"
            )
        field_spec = (entry.get("fields") or {}).get(field)
        if field_spec is None:
            raise ValueError(
                f"{entry['id']}: repeat observation operand {operand_name!r} "
                f"references unknown field {field!r}"
            )
        field_kind = str(field_spec.get("kind"))
        if field_kind != expected_field_kind:
            raise ValueError(
                f"{entry['id']}: repeat observation operand {operand_name!r} field {field!r} "
                f"has kind {field_kind!r}, expected {expected_field_kind!r}"
            )
        field_expr = f"Some('{field}')"

    return (
        f"Some(RepeatObservation::{rust_variant(kind)} {{ "
        "operand: RepeatObservedOperand { "
        f"name: {rust_string(operand_name)}, field: {field_expr}, "
        f"location: RepeatOperandLocation::{location} "
        "} "
        "})"
    )


def generated_destination_overlap(
    entry: dict[str, Any], operands: list[dict[str, Any]]
) -> str:
    relations = entry.get("destination_overlap") or []
    operands_by_name = {str(operand["name"]): operand for operand in operands}
    rows: list[str] = []
    for relation in relations:
        operand_names = relation.get("operands")
        if not isinstance(operand_names, list) or len(operand_names) != 2:
            raise ValueError(
                f"{entry['id']}: destination_overlap must name exactly two operands"
            )
        names = [str(name) for name in operand_names]
        operand_fields: list[str] = []
        for name in names:
            operand = operands_by_name.get(name)
            if operand is None:
                raise ValueError(
                    f"{entry['id']}: destination_overlap names unknown operand {name!r}"
                )
            field = operand.get("field")
            if not isinstance(field, str) or len(field) != 1:
                raise ValueError(
                    f"{entry['id']}: overlapping operand {name!r} has no encoded field"
                )
            if field not in (entry.get("fields") or {}):
                raise ValueError(
                    f"{entry['id']}: overlapping operand {name!r} field {field!r} "
                    "is not generated"
                )
            operand_fields.append(field)

        rule = str(relation.get("rule", ""))
        if rule not in {"same_value", "illegal_instruction"}:
            raise ValueError(
                f"{entry['id']}: unknown destination_overlap rule {rule!r}"
            )
        rows.append(
            "GeneratedDestinationOverlap { "
            f"operands: [{rust_string(names[0])}, {rust_string(names[1])}], "
            f"operand_fields: ['{operand_fields[0]}', '{operand_fields[1]}'], "
            f"rule: DestinationOverlapRule::{rust_variant(rule)} "
            "}"
        )
    return "&[" + ", ".join(rows) + "]"


def generated_ea_fields(entry: dict[str, Any], operands: list[dict[str, Any]]) -> str:
    fields = entry.get("fields") or {}
    operand_ordinals: dict[str, tuple[int, str, bool]] = {}
    for ordinal, operand in enumerate(operands):
        field = operand.get("field")
        if field is None:
            continue
        if not isinstance(field, str) or len(field) != 1:
            raise ValueError(
                f"{entry['id']}: operand {operand.get('name')!r} has invalid field {field!r}"
            )
        if field not in fields:
            raise ValueError(
                f"{entry['id']}: operand {operand.get('name')!r} references unknown field {field!r}"
            )
        if field in operand_ordinals:
            raise ValueError(
                f"{entry['id']}: field {field!r} is assigned to multiple syntax operands"
            )
        if ordinal > 0xFF:
            raise ValueError(f"{entry['id']}: syntax operand ordinal exceeds u8")
        if str(fields[field].get("kind", "")).lower() != "ea7":
            continue
        profile = str(operand.get("profile", ""))
        if profile not in {"ea", "fea", "vea"}:
            raise ValueError(
                f"{entry['id']}: EA operand {operand.get('name')!r} has unknown "
                f"profile {profile!r}"
            )
        operand_ordinals[field] = (
            ordinal,
            profile,
            str(operand.get("access", "")) in {"write", "read_write"},
        )

    rows: list[str] = []
    for symbol, spec in fields.items():
        if str(spec.get("kind", "")).lower() != "ea7":
            continue
        resolved = operand_ordinals.get(str(symbol))
        if resolved is None:
            raise ValueError(
                f"{entry['id']}: EA field {symbol!r} has no canonical syntax operand"
            )
        ordinal, profile, writes = resolved
        rows.append(
            "GeneratedEaField { "
            f"symbol: '{symbol}', syntax_operand_ordinal: {ordinal}, "
            f"profile: crate::EffectiveAddressProfile::{rust_variant(profile)}, "
            f"writes: {str(writes).lower()} "
            "}"
        )
    return "&[" + ", ".join(rows) + "]"


def _matches_concrete_pattern(value: str, pattern: str) -> bool:
    return all(
        expected in "x?" or actual == expected
        for actual, expected in zip(value, pattern, strict=True)
    )


def operator_space_prefix_cases(
    prefix_bits: int,
    prefixes: tuple[Any, ...],
    encoding_classes_by_name: dict[str, Any],
    resolver: Any,
) -> tuple[tuple[str, int, str | None], ...]:
    cases: list[tuple[str, int, str | None]] = []
    encoding_classes = tuple(
        dict.fromkeys(allocation.encoding_class for allocation in prefixes)
    )
    for encoding_class in encoding_classes:
        selectors = encoding_classes_by_name[encoding_class].selectors
        for prefix in range(1 << prefix_bits):
            bits = f"{prefix:0{prefix_bits}b}"
            if not any(
                _matches_concrete_pattern(bits[: len(selector)], selector)
                for selector in selectors
            ):
                continue
            cases.append((encoding_class, prefix, resolver(encoding_class, bits)))
    return tuple(cases)


def render_operator_space_matcher(
    prefix_bits: int,
    prefixes: tuple[Any, ...],
    test_cases: tuple[tuple[str, int, str | None], ...],
) -> list[str]:
    rules: list[str] = []
    for allocation in prefixes:
        mask, value = pattern_mask_value(allocation.pattern)
        rules.append(
            "    ("
            f"EncodingClass::{RUST_ENCODING_CLASSES[allocation.encoding_class]}, "
            f"0x{mask:04x}, 0x{value:04x}, "
            f"OperatorSpace::{rust_variant(allocation.operator_space)}"
            "),"
        )
    cases = [
        "    ("
        f"EncodingClass::{RUST_ENCODING_CLASSES[encoding_class]}, "
        f"0x{prefix:04x}, "
        + (
            "None"
            if operator_space is None
            else f"Some(OperatorSpace::{rust_variant(operator_space)})"
        )
        + "),"
        for encoding_class, prefix, operator_space in test_cases
    ]
    return [
        "static OPERATOR_SPACE_PREFIX_RULES: &[(EncodingClass, u16, u16, OperatorSpace)] = &[",
        *rules,
        "];",
        "",
        "#[cfg(test)]",
        "pub(crate) static OPERATOR_SPACE_PREFIX_CASES: &[(EncodingClass, u16, Option<OperatorSpace>)] = &[",
        *cases,
        "];",
        "",
        "pub(crate) fn operator_space_from_prefix(",
        "    class: EncodingClass,",
        "    prefix: u16,",
        ") -> Option<OperatorSpace> {",
        f"    if prefix >= (1u16 << {prefix_bits}) {{",
        "        return None;",
        "    }",
        "    OPERATOR_SPACE_PREFIX_RULES.iter().find_map(",
        "        |(rule_class, mask, value, operator_space)| {",
        "            (*rule_class == class && prefix & *mask == *value).then_some(*operator_space)",
        "        },",
        "    )",
        "}",
        "",
    ]


def render(isa_design: Path) -> str:
    tool_dir = isa_design / "isa" / "tools"
    sys.path.insert(0, str(tool_dir))
    from defs_loader import load_operand_types  # type: ignore
    from encoding_architecture import (  # type: ignore
        ENCODING_CLASSES_BY_NAME,
        OPERATOR_SPACE_PREFIX_BITS,
        OPERATOR_SPACE_PREFIXES,
        operator_space_from_prefix,
    )
    from encoding_store import class_entries, load_encoding_store  # type: ignore
    from validate_alloc import compact_bits, validate_store  # type: ignore

    defs_root = isa_design / "isa" / "instructions" / "definitions"
    store = load_encoding_store(defs_root)
    operand_types = load_operand_types(defs_root)
    operands_by_form = {
        located.form.id: [
            {
                "name": operand.name,
                "type": operand.type,
                "access": operand.access,
                "field": operand.field,
                "profile": operand_types[operand.type].get("profile", ""),
            }
            for operand in located.form.operands
        ]
        for located in store.encodings
    }
    class_data = [
        {
            "class": encoding_class.name,
            # GeneratedForm keeps the historical Rust-facing field name, but
            # its value is the allocation width owned by EncodingClass.
            "payload_bits": encoding_class.allocation_bits,
            "entries": class_entries(store, encoding_class.name),
        }
        for encoding_class in store.classes
    ]
    definitions, definition_paths = load_definitions(isa_design)
    opcode_variants = {name: rust_variant(name) for name in definitions}
    allocation_summaries: dict[str, dict[str, int]] = {}
    for cls, summary, _skipped, overlaps in validate_store(defs_root):
        if overlaps:
            raise ValueError(f"{cls}: allocation overlaps: {overlaps[:5]}")
        allocation_summaries[cls] = summary

    source_paths = sorted(defs_root.glob("**/*.yaml"))
    ea_definition = (
        isa_design / "isa" / "addressing" / "effective_address" / "definition.yaml"
    )
    source_hash = digest_inputs(source_paths + definition_paths + [ea_definition])
    out = [
        "// @generated by tools/gen_isa.py; do not edit by hand.",
        "use crate::table::{",
        "    ConstraintPredicate, DestinationOverlapRule, EncodingClass, FieldKind, FlagsEffect,",
        "    GeneratedAttributes, GeneratedConstraint, GeneratedDestinationOverlap, GeneratedEaField,",
        "    GeneratedField, GeneratedForm, InstructionSet, OperatorSpace, RepeatObservation,",
        "    RepeatObservedOperand,",
        "    RepeatOperandLocation,",
        "};",
        "pub const ISA_INPUT_SHA256: &str =",
        f"    {rust_string(source_hash)};",
        "",
    ]

    out.extend([
        "#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]",
        "pub enum Opcode {",
        *[f"    {opcode_variants[name]}," for name in sorted(opcode_variants)],
        "}",
        "",
    ])
    out.extend(
        render_operator_space_matcher(
            OPERATOR_SPACE_PREFIX_BITS,
            OPERATOR_SPACE_PREFIXES,
            operator_space_prefix_cases(
                OPERATOR_SPACE_PREFIX_BITS,
                OPERATOR_SPACE_PREFIXES,
                ENCODING_CLASSES_BY_NAME,
                operator_space_from_prefix,
            ),
        )
    )

    form_names: list[str] = []
    seen_form_names: set[str] = set()
    descriptors: list[str] = []
    class_cubes: dict[str, list[tuple[int, int, int]]] = {name: [] for name in CLASS_ORDER}
    class_bits: dict[str, int] = {}
    for data in class_data:
        class_name = str(data["class"])
        payload_bits = int(data["payload_bits"])
        class_bits[class_name] = payload_bits
        for index, entry in enumerate(data.get("entries") or []):
            entry_id = str(entry["id"])
            text = str(entry["text"])
            mnemonic_name = mnemonic(text)
            definition = definitions.get(mnemonic_name)
            if definition is None:
                raise ValueError(f"{entry_id}: missing definition for {mnemonic_name}")
            pattern = compact_bits(str(entry["bits"]))
            mask, value = pattern_mask_value(pattern)
            fixed_bytes = fixed_operand_bytes(entry_id, operands_by_form[entry_id])
            variant = rust_variant(entry_id)
            if variant in seen_form_names:
                raise ValueError(f"duplicate generated FormId variant {variant} from {entry_id}")
            seen_form_names.add(variant)
            form_names.append(f"    {variant},")
            form_index = len(form_names) - 1
            class_cubes[class_name].extend(
                accepted_cubes(entry, pattern, mask, value, form_index)
            )

            field_rows: list[str] = []
            for symbol, spec in (entry.get("fields") or {}).items():
                field_rows.append(
                    "GeneratedField { "
                    f"symbol: '{symbol}', kind: FieldKind::{rust_variant(str(spec['kind']))}, "
                    f"width: {int(spec['width'])} "
                    "}"
                )
            fields = "&[" + ", ".join(field_rows) + "]"
            ea_fields = generated_ea_fields(entry, operands_by_form[entry_id])

            constraint_rows: list[str] = []
            for constraint in entry.get("constraints") or []:
                reason = rust_string(str(constraint.get("reason", "constraint")))
                if "allow" in constraint:
                    ranges = ", ".join(
                        f"({lo}, {hi})" for lo, hi in map(parse_range, constraint["allow"])
                    )
                    constraint_rows.append(
                        "GeneratedConstraint::Allow { "
                        f"field: '{constraint['field']}', ranges: &[{ranges}], reason: {reason} "
                        "}"
                    )
                else:
                    field = constraint.get("field")
                    field_expr = "None" if field is None else f"Some('{field}')"
                    constraint_rows.append(
                        "GeneratedConstraint::Exclude { "
                        f"field: {field_expr}, destination: {str(bool(constraint.get('destination'))).lower()}, "
                        f"predicate: ConstraintPredicate::{rust_variant(str(constraint['exclude']))}, reason: {reason} "
                        "}"
                    )
            constraints = "&[" + ", ".join(constraint_rows) + "]"
            destination_overlap = generated_destination_overlap(
                entry, operands_by_form[entry_id]
            )

            descriptors.append(
                "    GeneratedForm { "
                f"form: FormId::{variant}, id: {rust_string(entry_id)}, "
                f"opcode: Opcode::{opcode_variants[mnemonic_name]}, text: {rust_string(text)}, "
                f"class: EncodingClass::{RUST_ENCODING_CLASSES[class_name]}, "
                f"payload_bits: {payload_bits}, fixed_operand_bytes: {fixed_bytes}, "
                f"pattern: {rust_string(pattern)}, "
                f"mask: 0x{mask:x}, value: 0x{value:x}, fields: {fields}, ea_fields: {ea_fields}, "
                f"constraints: {constraints}, "
                f"destination_overlap: {destination_overlap}, "
                f"attributes: {generated_attributes(definition, entry, operands_by_form[entry_id])} "
                "},"
            )

    for class_name, cubes in class_cubes.items():
        bits = class_bits[class_name]
        cardinality = sum(1 << (bits - mask.bit_count()) for mask, _, _ in cubes)
        expected = allocation_summaries[class_name]["allocated"]
        if cardinality != expected:
            raise ValueError(
                f"{class_name}: generated decode cubes cover {cardinality} payloads, expected {expected}"
            )

    out.extend(
        [
            "#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]",
            "#[rustfmt::skip]",
            "pub enum FormId {",
            *form_names,
            "}",
            "",
            "#[derive(Debug, Clone, Copy)]",
            "struct DecodeTable {",
            "    shift: u8,",
            "    mask: u8,",
            "    offset: u32,",
            "}",
            "",
        ]
    )
    out.extend(render_direct_table("EXTRASHORT", class_bits["extrashort"], class_cubes["extrashort"]))
    out.extend(render_direct_table("SHORT", class_bits["short"], class_cubes["short"]))
    out.extend(render_direct_table("MEDIUM", class_bits["medium"], class_cubes["medium"]))
    out.extend(render_hierarchical_lookup("LONG", class_bits["long"], class_cubes["long"]))
    out.extend(
        render_hierarchical_lookup("EXTRALONG", class_bits["extralong"], class_cubes["extralong"])
    )
    out.extend(
        render_hierarchical_lookup("XXLONG", class_bits["xxlong"], class_cubes["xxlong"])
    )
    out.extend(
        [
            "fn walk_hierarchical_lookup(",
            "    mut edge: u32,",
            "    payload: u64,",
            "    tables: &[DecodeTable],",
            "    edges: &[u32],",
            ") -> u16 {",
            "    loop {",
            "        if edge == 0 {",
            "            return 0;",
            "        }",
            "        if edge & 0x8000_0000 != 0 {",
            "            return (edge & 0x7fff_ffff) as u16;",
            "        }",
            "        let table = tables[(edge - 1) as usize];",
            "        let index = ((payload >> table.shift) & u64::from(table.mask)) as usize;",
            "        edge = edges[table.offset as usize + index];",
            "    }",
            "}",
            "",
            "pub fn decode_form(class: EncodingClass, payload: u64) -> Option<&'static GeneratedForm> {",
            "    let encoded = match class {",
            "        EncodingClass::ExtraShort => EXTRASHORT_LOOKUP[payload as usize],",
            "        EncodingClass::Short => SHORT_LOOKUP[payload as usize],",
            "        EncodingClass::Medium => {",
            "            let page = MEDIUM_PAGE_INDEX[(payload >> 8) as usize] as usize;",
            "            MEDIUM_PAGES[page][(payload & 0xff) as usize]",
            "        }",
            "        EncodingClass::Long => {",
            "            walk_hierarchical_lookup(LONG_ROOT, payload, &LONG_TABLES, &LONG_EDGES)",
            "        }",
            "        EncodingClass::ExtraLong => {",
            "            walk_hierarchical_lookup(EXTRALONG_ROOT, payload, &EXTRALONG_TABLES, &EXTRALONG_EDGES)",
            "        }",
            "        EncodingClass::Xxlong => {",
            "            walk_hierarchical_lookup(XXLONG_ROOT, payload, &XXLONG_TABLES, &XXLONG_EDGES)",
            "        }",
            "    };",
            "    encoded",
            "        .checked_sub(1)",
            "        .map(|index| &GENERATED_FORMS[index as usize])",
            "}",
            "",
            "#[rustfmt::skip]",
            "pub static GENERATED_FORMS: &[GeneratedForm] = &[",
            *descriptors,
            "];",
            "",
        ]
    )
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--isa-design",
        type=Path,
        default=REPOSITORY_ROOT,
        help="ISA design repository root (default: this repository)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="generated Rust table path outside repository src directories",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the existing generated table is stale",
    )
    args = parser.parse_args()

    try:
        output = validated_output_path(args.output)
    except ValueError as error:
        parser.error(str(error))

    rendered = render(args.isa_design.resolve())
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != rendered:
            print(f"generated ISA table is stale: {output}", file=sys.stderr)
            return 1
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(f"generated {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
