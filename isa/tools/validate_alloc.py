#!/usr/bin/env python3
"""Validate hand-authored ISA allocation YAML files."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment error path
    raise SystemExit("PyYAML is required to validate allocation YAML files") from exc


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


def is_rn_direct(value: int) -> bool:
    return 0x00 <= value <= 0x0F


def is_sp_direct(value: int) -> bool:
    return value == 0x68


def is_reg_direct(value: int) -> bool:
    return is_rn_direct(value) or is_sp_direct(value)


def is_immediate(value: int) -> bool:
    return 0x6C <= value <= 0x6F


PREDICATES = {
    "rn_direct": is_rn_direct,
    "sp_direct": is_sp_direct,
    "reg_direct": is_reg_direct,
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

    if constraint.get("destination"):
        for field in ("d", "e"):
            field_bits, width = field_value(value, pattern, field)
            if width == 7:
                return predicate(field_bits)
        raise ValueError("destination constraint needs a 7-bit d or e EA field")

    field = constraint["field"]
    field_bits, width = field_value(value, pattern, field)
    if width == 0:
        raise ValueError(f"constraint references missing field {field!r}")
    return predicate(field_bits)


def entry_claims(
    path: Path,
    payload_bits: int,
    namespaces: list[str],
    entry: dict[str, Any],
) -> tuple[list[tuple[int, Claim]], Counter[str]]:
    entry_id = str(entry["id"])
    text = str(entry.get("text", ""))
    pattern = compact_bits(str(entry["bits"]))
    constraints = entry.get("constraints") or []

    if ";" in text:
        raise ValueError(f"{entry_id}: text must not contain semicolon notes; use constraints or notes")
    if len(pattern) != payload_bits:
        raise ValueError(f"{entry_id}: pattern has {len(pattern)} bits, expected {payload_bits}")

    declared_fields = entry.get("fields") or {}
    actual_fields = field_widths(pattern)
    for name, spec in declared_fields.items():
        expected_width = int(spec["width"])
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


def default_namespace_patterns(payload_bits: int, cls: str) -> list[str]:
    if cls == "medium":
        if payload_bits != 18:
            raise ValueError(f"medium payload_bits must be 18, got {payload_bits}")
        return [
            "0?????????????????",
            "10????????????????",
            "110???????????????",
            "1110??????????????",
        ]
    if cls == "long":
        if payload_bits != 26:
            raise ValueError(f"long payload_bits must be 26, got {payload_bits}")
        return [
            "111100????????????????????",
            "111101????????????????????",
            "111110????????????????????",
        ]
    if cls == "extralong":
        if payload_bits != 34:
            raise ValueError(f"extralong payload_bits must be 34, got {payload_bits}")
        return ["111111????????????????????????????"]
    return ["?" * payload_bits]


def namespace_patterns(payload_bits: int, data: dict[str, Any]) -> list[str]:
    raw = data.get("namespace")
    if raw is None:
        return default_namespace_patterns(payload_bits, str(data.get("class", "")))
    patterns = [compact_bits(str(item)) for item in raw]
    for pattern in patterns:
        if len(pattern) != payload_bits:
            raise ValueError(
                f"namespace pattern {pattern!r} has {len(pattern)} bits, expected {payload_bits}"
            )
    return patterns


def namespace_size(patterns: list[str]) -> int:
    seen: set[int] = set()
    total = 0
    for pattern in patterns:
        size = pattern_cardinality(pattern)
        if size <= (1 << 22):
            for value in expand_pattern(pattern):
                if value in seen:
                    raise ValueError(f"namespace overlap at 0x{value:x}")
                seen.add(value)
        total += size
    return total


def validate_file(path: Path) -> tuple[str, dict[str, int], Counter[str], list[str]]:
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping")
    if "escapes" in data:
        raise ValueError(f"{path}: top-level escapes are no longer supported; use class namespace patterns")

    cls = str(data["class"])
    payload_bits = int(data["payload_bits"])
    namespaces = namespace_patterns(payload_bits, data)
    total = namespace_size(namespaces)

    by_value: dict[int, Claim] = {}
    allocated_values: set[int] = set()
    skipped: Counter[str] = Counter()
    overlaps: list[str] = []
    for entry in data.get("entries") or []:
        claims, entry_skipped = entry_claims(path, payload_bits, namespaces, entry)
        skipped.update(entry_skipped)
        for value, claim in claims:
            previous = by_value.get(value)
            if previous is not None:
                overlaps.append(f"0x{value:x}: {previous.entry_id} overlaps {claim.entry_id}")
                continue
            by_value[value] = claim
            allocated_values.add(value)

    assigned = len(allocated_values)
    reserved_total = total - assigned
    summary = {
        "total": total,
        "allocated": assigned,
        "reserved_total": reserved_total,
        "claimed": len(by_value),
        "constraint_skipped": sum(skipped.values()),
    }
    return cls, summary, skipped, overlaps


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=sorted(Path("isa/alloc").glob("*.yaml")),
        help="allocation YAML files to validate",
    )
    args = parser.parse_args()

    had_error = False
    for path in args.paths:
        try:
            cls, summary, skipped, overlaps = validate_file(path)
        except Exception as exc:
            had_error = True
            print(f"{path}: ERROR: {exc}", file=sys.stderr)
            continue

        if overlaps:
            had_error = True
        print(f"{path} [{cls}]")
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
