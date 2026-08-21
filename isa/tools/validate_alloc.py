#!/usr/bin/env python3
"""Validate hand-authored ISA allocation YAML files."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import sys
from typing import Any, Iterable

from encoding_architecture import ARCHITECTURE_SOURCE_PATH


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DEFS_ROOT = REPOSITORY_ROOT / "isa" / "instructions" / "definitions"


@dataclass(frozen=True)
class Claim:
    path: Path
    entry_id: str
    text: str


def compact_bits(pattern: str) -> str:
    return "".join(pattern.split())


def parse_int(value: Any) -> int:
    if isinstance(value, int):
        return value
    text = str(value).replace("_", "")
    return int(text, 0)


def parse_range(value: Any) -> tuple[int, int]:
    text = str(value)
    if ".." in text:
        lo, hi = text.split("..", 1)
        return parse_int(lo), parse_int(hi)
    n = parse_int(text)
    return n, n


def pattern_cardinality(pattern: str) -> int:
    count = sum(1 for ch in pattern if ch not in "01")
    return 1 << count


def pattern_union_cardinality(patterns: Iterable[str]) -> int:
    """Return the exact cardinality of a union of allocation-pattern cubes."""
    compacted = tuple(
        sorted(
            {
                "".join(ch if ch in "01" else "?" for ch in compact_bits(pattern))
                for pattern in patterns
            }
        )
    )
    if not compacted:
        return 0
    width = len(compacted[0])
    if any(len(pattern) != width for pattern in compacted):
        raise ValueError("union patterns must have the same width")

    @lru_cache(maxsize=None)
    def count(index: int, active: tuple[str, ...]) -> int:
        remaining = width - index
        if any(pattern[index:] == "?" * remaining for pattern in active):
            return 1 << remaining
        if index == width:
            return 1
        zero = tuple(pattern for pattern in active if pattern[index] in "0?")
        one = tuple(pattern for pattern in active if pattern[index] in "1?")
        return (count(index + 1, zero) if zero else 0) + (
            count(index + 1, one) if one else 0
        )

    return count(0, compacted)


def expand_pattern(pattern: str) -> Iterable[int]:
    def rec(index: int, value: int) -> Iterable[int]:
        if index == len(pattern):
            yield value
            return
        ch = pattern[index]
        if ch == "0" or ch == "1":
            yield from rec(index + 1, (value << 1) | int(ch))
            return
        yield from rec(index + 1, value << 1)
        yield from rec(index + 1, (value << 1) | 1)

    yield from rec(0, 0)


def matches_pattern(value: int, pattern: str) -> bool:
    width = len(pattern)
    for index, ch in enumerate(pattern):
        if ch not in "01":
            continue
        bit = (value >> (width - index - 1)) & 1
        if bit != int(ch):
            return False
    return True


def field_widths(pattern: str) -> Counter[str]:
    widths: Counter[str] = Counter()
    for ch in pattern:
        if ch not in "01?":
            widths[ch] += 1
    return widths


def field_value(value: int, pattern: str, field: str) -> tuple[int, int]:
    width = len(pattern)
    out = 0
    count = 0
    for index, ch in enumerate(pattern):
        if ch != field:
            continue
        out = (out << 1) | ((value >> (width - index - 1)) & 1)
        count += 1
    return out, count


def is_immediate(value: int) -> bool:
    return 0x5B <= value <= 0x5E


PREDICATES = {
    "immediate": is_immediate,
}


def field_allowed(value: int, pattern: str, constraint: dict[str, Any]) -> bool:
    field = constraint["field"]
    field_bits, width = field_value(value, pattern, field)
    if width == 0:
        raise ValueError(f"constraint references missing field {field!r}")
    ranges = [parse_range(item) for item in constraint["allow"]]
    return any(lo <= field_bits <= hi for lo, hi in ranges)


def excluded_by(value: int, pattern: str, constraint: dict[str, Any]) -> bool:
    pred_name = constraint["exclude"]
    if pred_name not in PREDICATES:
        raise ValueError(f"unknown exclude predicate {pred_name!r}")
    predicate = PREDICATES[pred_name]

    field = constraint["field"]
    field_bits, width = field_value(value, pattern, field)
    if width == 0:
        raise ValueError(f"constraint references missing field {field!r}")
    return predicate(field_bits)


def entry_claims(
    path: Path,
    allocation_bits: int,
    namespaces: list[str],
    entry: dict[str, Any],
) -> tuple[list[tuple[int, Claim]], Counter[str]]:
    entry_id = str(entry["id"])
    text = str(entry.get("text", ""))
    pattern = compact_bits(str(entry["bits"]))
    constraints = entry.get("constraints") or []

    if len(pattern) != allocation_bits:
        raise ValueError(f"{entry_id}: pattern has {len(pattern)} bits, expected {allocation_bits}")

    declared_fields = entry.get("fields") or {}
    actual_fields = field_widths(pattern)
    for name, spec in declared_fields.items():
        expected_width = int(spec.get("width", actual_fields.get(name, 0)))
        actual_width = actual_fields.get(name, 0)
        if actual_width != expected_width:
            raise ValueError(
                f"{entry_id}: field {name!r} width is {actual_width}, declared {expected_width}"
            )

    claims: list[tuple[int, Claim]] = []
    skipped: Counter[str] = Counter()
    claim = Claim(path=path, entry_id=entry_id, text=text)
    for value in expand_pattern(pattern):
        if not any(matches_pattern(value, namespace) for namespace in namespaces):
            raise ValueError(f"{entry_id}: value 0x{value:x} is outside class namespace")

        skip_reason = None
        for constraint in constraints:
            if "allow" in constraint and not field_allowed(value, pattern, constraint):
                skip_reason = str(constraint.get("reason", "allow_constraint"))
                break
            if "exclude" in constraint and excluded_by(value, pattern, constraint):
                skip_reason = str(constraint.get("reason", constraint["exclude"]))
                break

        if skip_reason is not None:
            skipped[skip_reason] += 1
            continue
        claims.append((value, claim))

    return claims, skipped


def _fixed_value(pattern: str) -> int:
    value = 0
    for ch in pattern:
        value = (value << 1) | (1 if ch == "1" else 0)
    return value


def _free_positions(pattern: str) -> set[int]:
    return {index for index, ch in enumerate(pattern) if ch not in "01"}


def _constraint_positions(pattern: str, constraints: list[dict[str, Any]]) -> set[int]:
    fields = {str(constraint["field"]) for constraint in constraints}
    return {index for index, ch in enumerate(pattern) if ch in fields}


def _set_position(value: int, width: int, position: int, bit: int) -> int:
    shift = width - position - 1
    return (value | (1 << shift)) if bit else (value & ~(1 << shift))


def _constraint_skip_reason(
    value: int, pattern: str, constraints: list[dict[str, Any]]
) -> str | None:
    for constraint in constraints:
        if "allow" in constraint and not field_allowed(value, pattern, constraint):
            return str(constraint.get("reason", "allow_constraint"))
        if "exclude" in constraint and excluded_by(value, pattern, constraint):
            return str(constraint.get("reason", constraint["exclude"]))
    return None


def _pattern_subset_of(pattern: str, namespace: str) -> bool:
    return all(
        namespace_bit not in "01" or pattern_bit == namespace_bit
        for pattern_bit, namespace_bit in zip(pattern, namespace)
    )


def entry_claim_summary(
    path: Path,
    allocation_bits: int,
    namespaces: list[str],
    entry: dict[str, Any],
) -> tuple[int, Counter[str], Claim]:
    """Return exact legal cardinality without expanding unconstrained operand bits."""
    patterns, skipped, claim = entry_claim_patterns(
        path, allocation_bits, namespaces, entry
    )
    return sum(pattern_cardinality(pattern) for pattern in patterns), skipped, claim


def entry_claim_patterns(
    path: Path,
    allocation_bits: int,
    namespaces: list[str],
    entry: dict[str, Any],
) -> tuple[list[str], Counter[str], Claim]:
    """Return disjoint legal subcubes split only across constrained fields."""
    entry_id = str(entry["id"])
    text = str(entry.get("text", ""))
    pattern = compact_bits(str(entry["bits"]))
    constraints = entry.get("constraints") or []
    if len(pattern) != allocation_bits:
        raise ValueError(f"{entry_id}: pattern has {len(pattern)} bits, expected {allocation_bits}")
    if not any(_pattern_subset_of(pattern, namespace) for namespace in namespaces):
        raise ValueError(f"{entry_id}: pattern is outside class namespace")

    declared_fields = entry.get("fields") or {}
    actual_fields = field_widths(pattern)
    for name, spec in declared_fields.items():
        expected_width = int(spec.get("width", actual_fields.get(name, 0)))
        actual_width = actual_fields.get(name, 0)
        if actual_width != expected_width:
            raise ValueError(
                f"{entry_id}: field {name!r} width is {actual_width}, declared {expected_width}"
            )

    constrained = sorted(_constraint_positions(pattern, constraints))
    free = _free_positions(pattern)
    if not set(constrained) <= free:
        # Fixed bits may be named only when another overlapping pattern fixes them;
        # within one entry every declared field remains variable.
        raise ValueError(f"{entry_id}: constraint field includes fixed opcode bits")
    multiplier = 1 << (len(free) - len(constrained))
    legal_patterns: list[str] = []
    skipped: Counter[str] = Counter()
    base = _fixed_value(pattern)
    for assignment in range(1 << len(constrained)):
        value = base
        for bit_index, position in enumerate(constrained):
            value = _set_position(value, allocation_bits, position, (assignment >> bit_index) & 1)
        reason = _constraint_skip_reason(value, pattern, constraints)
        if reason is None:
            chars = [ch if ch in "01" else "?" for ch in pattern]
            for position in constrained:
                shift = allocation_bits - position - 1
                chars[position] = "1" if value & (1 << shift) else "0"
            legal_patterns.append("".join(chars))
        else:
            skipped[reason] += multiplier
    return legal_patterns, skipped, Claim(path=path, entry_id=entry_id, text=text)


def entries_overlap(
    left: dict[str, Any], right: dict[str, Any]
) -> int | None:
    """Return the least deterministic legal witness, or None when two entries are disjoint."""
    left_pattern = compact_bits(str(left["bits"]))
    right_pattern = compact_bits(str(right["bits"]))
    if len(left_pattern) != len(right_pattern):
        return None
    width = len(left_pattern)
    base = 0
    combined_free: set[int] = set()
    for index, (left_bit, right_bit) in enumerate(zip(left_pattern, right_pattern)):
        if left_bit in "01" and right_bit in "01" and left_bit != right_bit:
            return None
        fixed = left_bit if left_bit in "01" else right_bit if right_bit in "01" else None
        if fixed is None:
            combined_free.add(index)
        elif fixed == "1":
            base = _set_position(base, width, index, 1)

    left_constraints = left.get("constraints") or []
    right_constraints = right.get("constraints") or []
    relevant = (
        _constraint_positions(left_pattern, left_constraints)
        | _constraint_positions(right_pattern, right_constraints)
    ) & combined_free
    positions = sorted(relevant)
    for assignment in range(1 << len(positions)):
        value = base
        for bit_index, position in enumerate(positions):
            value = _set_position(value, width, position, (assignment >> bit_index) & 1)
        if (
            _constraint_skip_reason(value, left_pattern, left_constraints) is None
            and _constraint_skip_reason(value, right_pattern, right_constraints) is None
        ):
            return value
    return None


def validate_store(defs_root: Path) -> list[tuple[str, dict[str, int], Counter[str], list[str]]]:
    """Validate all per-instruction encodings grouped by class."""
    from encoding_store import class_entries, load_encoding_store

    store = load_encoding_store(defs_root)
    results: list[tuple[str, dict[str, int], Counter[str], list[str]]] = []
    for encoding_class in store.classes:
        data = {
            "class": encoding_class.name,
            "allocation_bits": encoding_class.allocation_bits,
            "namespace": list(encoding_class.namespace),
            "entries": class_entries(store, encoding_class.name),
        }
        total = namespace_size(list(encoding_class.namespace))
        prior_entries: list[tuple[dict[str, Any], Claim]] = []
        allocated_count = 0
        skipped: Counter[str] = Counter()
        overlaps: list[str] = []
        for entry in data["entries"]:
            claim_count, entry_skipped, claim = entry_claim_summary(
                Path(str(entry.get("source_path", ARCHITECTURE_SOURCE_PATH))),
                encoding_class.allocation_bits,
                list(encoding_class.namespace),
                entry,
            )
            skipped.update(entry_skipped)
            for previous_entry, previous in prior_entries:
                witness = entries_overlap(previous_entry, entry)
                if witness is not None:
                    overlaps.append(
                        f"0x{witness:x}: {previous.entry_id} overlaps {claim.entry_id}"
                    )
            prior_entries.append((entry, claim))
            allocated_count += claim_count
        results.append(
            (
                encoding_class.name,
                {
                    "total": total,
                    "allocated": allocated_count,
                    "reserved_total": total - allocated_count,
                    "claimed": allocated_count,
                    "constraint_skipped": sum(skipped.values()),
                },
                skipped,
                overlaps,
            )
        )
    return results


def namespace_patterns(allocation_bits: int, data: dict[str, Any]) -> list[str]:
    raw = data.get("namespace")
    if raw is None:
        raise ValueError("namespace is required")
    patterns = [compact_bits(str(item)) for item in raw]
    for pattern in patterns:
        if len(pattern) != allocation_bits:
            raise ValueError(
                f"namespace pattern {pattern!r} has {len(pattern)} bits, expected {allocation_bits}"
            )
    return patterns


def namespace_size(patterns: list[str]) -> int:
    total = sum(pattern_cardinality(pattern) for pattern in patterns)
    union = pattern_union_cardinality(patterns)
    if union != total:
        raise ValueError("namespace patterns overlap")
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--defs",
        type=Path,
        default=DEFAULT_DEFS_ROOT,
        help=(
            "ISA definition root "
            "(default: repository isa/instructions/definitions)"
        ),
    )
    args = parser.parse_args()

    had_error = False
    try:
        results = [
            (None, cls, summary, skipped, overlaps)
            for cls, summary, skipped, overlaps in validate_store(args.defs)
        ]
    except Exception as exc:
        had_error = True
        print(f"{args.defs}: ERROR: {exc}", file=sys.stderr)
        results = []

    for path, cls, summary, skipped, overlaps in results:
        if overlaps:
            had_error = True
        print(f"{path or args.defs} [{cls}]")
        print(f"  allocated:          {summary['allocated']}")
        print(f"  reserved total:     {summary['reserved_total']}")
        print(f"  constraint skipped: {summary['constraint_skipped']}")
        print(f"  total namespace:    {summary['total']}")
        if skipped:
            details = ", ".join(f"{key}={value}" for key, value in sorted(skipped.items()))
            print(f"  skipped by reason:  {details}")
        print(f"  overlaps:           {len(overlaps)}")
        for item in overlaps[:20]:
            print(f"    {item}")

    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
