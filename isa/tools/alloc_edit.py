#!/usr/bin/env python3
"""Inspect opcode allocation space while editing hand-authored YAML tables."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import difflib
import os
from pathlib import Path
import re
import sys
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment error path
    raise SystemExit("PyYAML is required to inspect allocation YAML files") from exc

TOOL_DIR = Path(__file__).resolve().parent
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from validate_alloc import (  # noqa: E402
    Claim,
    compact_bits,
    entry_claims,
    excluded_by,
    expand_pattern,
    field_allowed,
    matches_pattern,
    namespace_patterns,
    namespace_size,
    pattern_cardinality,
)
from encoding_architecture import ARCHITECTURE_SOURCE_PATH  # noqa: E402


DEFAULT_DEFS_ROOT = Path("isa/defs")
DEFAULT_MAX_ENUMERATE = 5_000_000
ANSI_RESET = "\033[0m"
ANSI_DIM = "\033[2m"
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
FIELD_COLORS = {
    "size": "\033[96m",
    "rn": "\033[92m",
    "freg": "\033[92m",
    "ea7": "\033[93m",
    "condition": "\033[95m",
    "immediate": "\033[94m",
    "bits": "\033[90m",
}


@dataclass(frozen=True)
class SkippedSlot:
    entry_id: str
    reason: str
    text: str


@dataclass(frozen=True)
class Cube:
    mask: int
    value: int
    width: int

    @property
    def slots(self) -> int:
        return 1 << (self.width - self.mask.bit_count())


@dataclass
class AllocationSpace:
    path: Path
    cls: str
    payload_bits: int
    namespaces: list[str]
    entries: list[dict[str, Any]]
    allocated: dict[int, Claim]
    claimed: dict[int, Claim]
    skipped: dict[int, list[SkippedSlot]]


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping")
    return data


def load_space_data(path: Path, data: dict[str, Any]) -> AllocationSpace:
    cls = str(data["class"])
    payload_bits = int(data["payload_bits"])
    namespaces = namespace_patterns(payload_bits, data)
    if "escapes" in data:
        raise ValueError(f"{path}: top-level escapes are no longer supported; use class namespace patterns")
    entries = [entry for entry in data.get("entries") or [] if isinstance(entry, dict)]
    allocated: dict[int, Claim] = {}
    claimed: dict[int, Claim] = {}
    skipped: dict[int, list[SkippedSlot]] = defaultdict(list)
    overlap_count = 0
    overlap_examples: list[str] = []

    for entry in entries:
        entry_path = Path(str(entry.get("source_path", path)))
        claims, _entry_skipped = entry_claims(entry_path, payload_bits, namespaces, entry)
        for value, claim in claims:
            previous = claimed.get(value)
            if previous is not None:
                overlap_count += 1
                if len(overlap_examples) < 20:
                    digits = (payload_bits + 3) // 4
                    overlap_examples.append(
                        f"0x{value:0{digits}x}: {previous.entry_id} overlaps {claim.entry_id}"
                    )
                continue
            allocated[value] = claim
            claimed[value] = claim
        for value, reason in skipped_values(entry_path, payload_bits, namespaces, entry):
            skipped[value].append(
                SkippedSlot(
                    entry_id=str(entry["id"]),
                    reason=reason,
                    text=str(entry.get("text", "")),
                )
            )

    if overlap_count:
        detail = "\n  ".join(overlap_examples)
        raise ValueError(
            f"{path}: {overlap_count:,} overlapping allocated slots"
            + (f"; first overlaps:\n  {detail}" if detail else "")
        )

    return AllocationSpace(
        path=path,
        cls=cls,
        payload_bits=payload_bits,
        namespaces=namespaces,
        entries=entries,
        allocated=allocated,
        claimed=claimed,
        skipped=dict(skipped),
    )


def load_store_space(defs_root: Path, cls: str) -> AllocationSpace:
    from encoding_store import class_entries, load_encoding_store

    store = load_encoding_store(defs_root)
    encoding_class = store.classes_by_name.get(cls)
    if encoding_class is None:
        raise ValueError(f"unknown encoding class {cls!r}")
    return load_space_data(
        ARCHITECTURE_SOURCE_PATH,
        {
            "class": cls,
            "payload_bits": encoding_class.payload_bits,
            "namespace": list(encoding_class.namespace),
            "entries": class_entries(store, cls),
        },
    )


def skipped_values(
    path: Path,
    payload_bits: int,
    namespaces: list[str],
    entry: dict[str, Any],
) -> Iterable[tuple[int, str]]:
    entry_id = str(entry["id"])
    pattern = compact_bits(str(entry["bits"]))
    constraints = entry.get("constraints") or []
    if len(pattern) != payload_bits:
        raise ValueError(f"{entry_id}: pattern has {len(pattern)} bits, expected {payload_bits}")

    for value in expand_pattern(pattern):
        if not any(matches_pattern(value, namespace) for namespace in namespaces):
            raise ValueError(f"{entry_id}: value 0x{value:x} is outside class namespace")

        for constraint in constraints:
            if "allow" in constraint and not field_allowed(value, pattern, constraint):
                yield value, str(constraint.get("reason", "allow_constraint"))
                break
            if "exclude" in constraint and excluded_by(value, pattern, constraint):
                yield value, str(constraint.get("reason", constraint["exclude"]))
                break


def namespace_values(space: AllocationSpace, max_enumerate: int) -> set[int]:
    total = namespace_size(space.namespaces)
    if total > max_enumerate:
        raise ValueError(
            f"{space.cls}: namespace has {total:,} slots; pass --max-enumerate above that to enumerate holes"
        )
    out: set[int] = set()
    for pattern in space.namespaces:
        out.update(expand_pattern(pattern))
    return out


def normalize_pattern(pattern: str, width: int) -> str:
    out = compact_bits(pattern)
    if len(out) > width:
        raise ValueError(f"pattern has {len(out)} bits, expected at most {width}")
    out = "".join(ch if ch in "01" else "?" for ch in out)
    return out + "?" * (width - len(out))


def display_pattern(pattern: str, width: int) -> str:
    out = compact_bits(pattern)
    if len(out) > width:
        raise ValueError(f"pattern has {len(out)} bits, expected at most {width}")
    return out + "?" * (width - len(out))


def iter_pattern_values(pattern: str) -> Iterable[int]:
    return expand_pattern(pattern)


def contiguous_ranges(values: Iterable[int]) -> Iterable[tuple[int, int]]:
    iterator = iter(sorted(values))
    try:
        start = prev = next(iterator)
    except StopIteration:
        return
    for value in iterator:
        if value == prev + 1:
            prev = value
            continue
        yield start, prev
        start = prev = value
    yield start, prev


def aligned_blocks(start: int, end: int, width: int) -> Iterable[tuple[int, int]]:
    value = start
    while value <= end:
        remaining = end - value + 1
        if value == 0:
            size = 1 << (remaining.bit_length() - 1)
        else:
            size = value & -value
        while size > remaining:
            size >>= 1
        while size > (1 << width):
            size >>= 1
        yield value, size
        value += size


def block_pattern(base: int, size: int, width: int) -> str:
    wildcard_bits = size.bit_length() - 1
    bits = f"{base:0{width}b}"
    if wildcard_bits == 0:
        return bits
    return bits[:-wildcard_bits] + "?" * wildcard_bits


def cube_from_pattern(pattern: str) -> Cube:
    pattern = compact_bits(pattern)
    width = len(pattern)
    mask = 0
    value = 0
    for ch in pattern:
        mask <<= 1
        value <<= 1
        if ch == "?":
            continue
        mask |= 1
        if ch == "1":
            value |= 1
    return Cube(mask=mask, value=value, width=width)


def cube_pattern(cube: Cube) -> str:
    chars: list[str] = []
    for bit_index in range(cube.width - 1, -1, -1):
        bit = 1 << bit_index
        if cube.mask & bit:
            chars.append("1" if cube.value & bit else "0")
        else:
            chars.append("?")
    return "".join(chars)


def cube_min_value(cube: Cube) -> int:
    return cube.value


def values_to_aligned_cubes(values: Iterable[int], width: int) -> list[Cube]:
    cubes: list[Cube] = []
    for start, end in contiguous_ranges(values):
        for base, size in aligned_blocks(start, end, width):
            cubes.append(cube_from_pattern(block_pattern(base, size, width)))
    return cubes


def cube_to_espresso_input(cube: Cube) -> tuple[int, ...]:
    out: list[int] = []
    for bit_index in range(cube.width - 1, -1, -1):
        bit = 1 << bit_index
        if not cube.mask & bit:
            out.append(3)
        elif cube.value & bit:
            out.append(2)
        else:
            out.append(1)
    return tuple(out)


def espresso_input_to_cube(items: Iterable[int], width: int) -> Cube:
    mask = 0
    value = 0
    for item in items:
        mask <<= 1
        value <<= 1
        if item == 3:
            continue
        if item == 2:
            mask |= 1
            value |= 1
            continue
        if item == 1:
            mask |= 1
            continue
        raise ValueError(f"unexpected espresso cube item {item!r}")
    return Cube(mask=mask, value=value, width=width)


def espresso_minimize_cubes(cubes: Iterable[Cube], width: int) -> list[Cube]:
    try:
        from pyeda.boolalg.espresso import FTYPE, espresso
    except ImportError as exc:
        raise RuntimeError(
            "PyEDA is required for minimized hole/reserved covers. Install it with: "
            "CFLAGS='-Wno-incompatible-function-pointer-types' "
            "/opt/homebrew/anaconda3/bin/python3 -m pip install pyeda"
        ) from exc

    cover = [(cube_to_espresso_input(cube), (1,)) for cube in cubes]
    if not cover:
        return []
    minimized = espresso(width, 1, cover, FTYPE)
    return sorted(
        [espresso_input_to_cube(input_part, width) for input_part, output_part in minimized if output_part[0] == 1],
        key=lambda cube: (cube_min_value(cube), -cube.slots, cube_pattern(cube)),
    )


def minimize_disjoint_cubes(cubes: Iterable[Cube], width: int) -> list[Cube]:
    current = set(cubes)
    while True:
        next_cubes: set[Cube] = set()
        merge_count = 0
        groups: dict[int, set[int]] = defaultdict(set)
        for cube in current:
            groups[cube.mask].add(cube.value)

        for mask, values in groups.items():
            remaining = set(values)
            while True:
                best_bit = 0
                best_pairs: list[tuple[int, int]] = []
                bit = 1
                for _ in range(width):
                    if mask & bit:
                        pairs = [
                            (value, value ^ bit)
                            for value in remaining
                            if (value & bit) == 0 and (value ^ bit) in remaining
                        ]
                        if len(pairs) > len(best_pairs):
                            best_bit = bit
                            best_pairs = pairs
                    bit <<= 1
                if not best_pairs:
                    break

                new_mask = mask ^ best_bit
                for left, right in best_pairs:
                    if left not in remaining or right not in remaining:
                        continue
                    remaining.remove(left)
                    remaining.remove(right)
                    next_cubes.add(Cube(mask=new_mask, value=left & new_mask, width=width))
                    merge_count += 1

            for value in remaining:
                next_cubes.add(Cube(mask=mask, value=value, width=width))

        if merge_count == 0:
            return sorted(current, key=lambda cube: (cube_min_value(cube), -cube.slots, cube_pattern(cube)))
        current = next_cubes


def minimized_cubes_from_values(values: Iterable[int], width: int) -> list[Cube]:
    expected = set(values)
    cubes = espresso_minimize_cubes(values_to_aligned_cubes(expected, width), width)
    cubes = exact_disjoint_cubes(cubes, expected, width)
    validate_exact_cover(cubes, expected)
    return cubes


def covered_values(cubes: Iterable[Cube]) -> set[int]:
    out: set[int] = set()
    for cube in cubes:
        out.update(expand_pattern(cube_pattern(cube)))
    return out


def exact_disjoint_cubes(cubes: Iterable[Cube], expected: set[int], width: int) -> list[Cube]:
    remaining = set(expected)
    out: list[Cube] = []
    for cube in sorted(cubes, key=lambda item: (-item.slots, cube_min_value(item), cube_pattern(item))):
        cube_values = set(expand_pattern(cube_pattern(cube))) & remaining
        if not cube_values:
            continue
        out.extend(minimize_disjoint_cubes(values_to_aligned_cubes(cube_values, width), width))
        remaining.difference_update(cube_values)
    if remaining:
        out.extend(minimize_disjoint_cubes(values_to_aligned_cubes(remaining, width), width))
    return sorted(out, key=lambda cube: (cube_min_value(cube), -cube.slots, cube_pattern(cube)))


def validate_exact_cover(cubes: Iterable[Cube], expected: set[int]) -> None:
    covered: set[int] = set()
    for cube in cubes:
        cube_values = set(expand_pattern(cube_pattern(cube)))
        overlap = covered & cube_values
        if overlap:
            sample = min(overlap)
            raise RuntimeError(f"minimized cover has overlapping cubes at 0x{sample:x}")
        covered.update(cube_values)
    if covered != expected:
        missing = expected - covered
        extra = covered - expected
        if missing:
            raise RuntimeError(f"minimized cover missed 0x{min(missing):x}")
        raise RuntimeError(f"minimized cover includes off-set value 0x{min(extra):x}")


def value_range_text(base: int, size: int, width: int) -> str:
    if size == 1:
        return f"0x{base:0{(width + 3) // 4}x}"
    end = base + size - 1
    return f"0x{base:0{(width + 3) // 4}x}..0x{end:0{(width + 3) // 4}x}"


def cube_span_text(cube: Cube) -> str:
    digits = (cube.width + 3) // 4
    lo = cube.value
    hi = cube.value | (((1 << cube.width) - 1) ^ cube.mask)
    if lo == hi:
        return f"0x{lo:0{digits}x}"
    return f"0x{lo:0{digits}x}..0x{hi:0{digits}x}"


def pattern_min_value(pattern: str) -> int:
    value = 0
    for ch in pattern:
        value = (value << 1) | (1 if ch == "1" else 0)
    return value


def render_synthetic_cubes(
    rows: list[tuple[int, int, list[str]]],
    *,
    kind: str,
    order: int,
    values: set[int],
    payload_bits: int,
    use_color: bool,
    limit: int,
    hidden_counts: Counter[str],
) -> None:
    if not values:
        return
    blocks = minimized_cubes_from_values(values, payload_bits)
    if limit and len(blocks) > limit:
        hidden_counts[kind] += len(blocks) - limit
        blocks = blocks[:limit]
    for index, cube in enumerate(blocks, start=1):
        pattern = cube_pattern(cube)
        rows.append(
            (
                cube_min_value(cube),
                order,
                [
                    f"{kind}.{index}",
                    colorize_bits(pattern, {}, use_color),
                    f"{cube.slots:,}",
                    f"{cube.slots:,}",
                    "0",
                    f"{kind} ; span {cube_span_text(cube)}",
                ],
            )
        )


def visible_len(text: str) -> int:
    return len(ANSI_RE.sub("", text))


def pad_visible(text: str, width: int) -> str:
    return text + " " * max(0, width - visible_len(text))


def color_enabled(args: argparse.Namespace) -> bool:
    mode = getattr(args, "color", "auto")
    if mode == "always":
        return True
    if mode == "never":
        return False
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


def colorize_bits(pattern: str, fields: dict[str, Any] | None, use_color: bool) -> str:
    if not use_color:
        return pattern
    fields = fields or {}
    out: list[str] = []
    for ch in pattern:
        if ch == "?":
            out.append(f"{ANSI_DIM}?{ANSI_RESET}")
            continue
        if ch in "01":
            out.append(ch)
            continue
        kind = field_kind(fields, ch)
        color = FIELD_COLORS.get(kind or "", FIELD_COLORS["bits"])
        out.append(f"{color}{ch}{ANSI_RESET}")
    return "".join(out)


def field_kind(fields: dict[str, Any], symbol: str) -> str | None:
    spec = fields.get(symbol)
    if isinstance(spec, dict):
        kind = spec.get("kind")
        return str(kind) if kind is not None else None
    return None


def infer_fields(pattern: str) -> dict[str, dict[str, Any]]:
    widths: Counter[str] = Counter(ch for ch in pattern if ch not in "01?")
    fields: dict[str, dict[str, Any]] = {}
    for symbol, width in widths.items():
        if symbol == "z":
            kind = "size"
        elif symbol == "c":
            kind = "condition"
        elif symbol == "i":
            kind = "immediate"
        elif width == 7:
            kind = "ea7"
        elif width == 4:
            kind = "rn"
        else:
            kind = "bits"
        fields[symbol] = {"kind": kind, "width": width}
    return fields


def format_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "(none)"
    widths = [max(visible_len(headers[i]), *(visible_len(row[i]) for row in rows)) for i in range(len(headers))]
    lines = [
        "  ".join(pad_visible(headers[i], widths[i]) for i in range(len(headers))),
        "  ".join("-" * widths[i] for i in range(len(headers))),
    ]
    for row in rows:
        lines.append("  ".join(pad_visible(row[i], widths[i]) for i in range(len(headers))))
    return "\n".join(lines)


def command_summary(args: argparse.Namespace) -> int:
    rows: list[list[str]] = []
    from encoding_store import load_encoding_store

    store = load_encoding_store(args.defs_root)
    for encoding_class in store.classes:
        space = load_store_space(args.defs_root, encoding_class.name)
        total = namespace_size(space.namespaces)
        allocated = len(space.allocated)
        skipped = sum(len(items) for items in space.skipped.values())
        unavailable = set(space.claimed)
        unavailable.update(space.skipped)
        rows.append(
            [
                space.cls,
                str(space.payload_bits),
                f"{total:,}",
                f"{allocated:,}",
                f"{skipped:,}",
                f"{total - len(unavailable):,}",
                str(ARCHITECTURE_SOURCE_PATH),
            ]
        )
    print(format_table(["class", "bits", "namespace", "allocated", "reclaimed", "clean-free", "path"], rows))
    return 0


def command_legend(args: argparse.Namespace) -> int:
    use_color = color_enabled(args)
    rows = []
    samples = [
        ("size", "zz"),
        ("rn", "rrrr"),
        ("freg", "ffff"),
        ("ea7", "eeeeeee"),
        ("condition", "cccc"),
        ("immediate", "iiiiiiii"),
        ("bits", "xxxx"),
    ]
    for kind, pattern in samples:
        fields = {pattern[0]: {"kind": kind}}
        sample = colorize_bits(pattern, fields, use_color)
        rows.append([kind, sample])
    rows.append(["fixed", "0101"])
    rows.append(["wildcard", colorize_bits("????", {}, use_color)])
    print(format_table(["kind", "sample"], rows))
    return 0


def command_entries(args: argparse.Namespace) -> int:
    space = load_store_space(args.defs_root, args.cls)
    leading = normalize_pattern(args.leading, space.payload_bits) if args.leading else None
    needle = args.grep.lower() if args.grep else None
    use_color = color_enabled(args)
    rows: list[tuple[int, int, list[str]]] = []
    for entry in space.entries:
        bits = compact_bits(str(entry["bits"]))
        text = str(entry.get("text", ""))
        entry_id = str(entry["id"])
        if leading and not patterns_overlap(bits, leading):
            continue
        if needle and needle not in entry_id.lower() and needle not in text.lower():
            continue
        entry_path = Path(str(entry.get("source_path", space.path)))
        claims, skipped = entry_claims(
            entry_path, space.payload_bits, space.namespaces, entry
        )
        rows.append(
            (
                pattern_min_value(bits),
                0,
                [
                entry_id,
                colorize_bits(bits, entry.get("fields") or {}, use_color),
                f"{pattern_cardinality(bits):,}",
                f"{len(claims):,}",
                f"{sum(skipped.values()):,}",
                text,
                ],
            )
        )

    hidden_counts: Counter[str] = Counter()
    if args.show_reserved:
        all_values = namespace_values(space, args.max_enumerate)
        skipped_values_set = set(space.skipped)
        reserved_values = all_values - set(space.claimed) - skipped_values_set
        reclaimed_values = skipped_values_set - set(space.claimed)
        if leading:
            reserved_values = {value for value in reserved_values if matches_pattern(value, leading)}
            reclaimed_values = {value for value in reclaimed_values if matches_pattern(value, leading)}

        if needle is None or needle in "reclaimed":
            render_synthetic_cubes(
                rows,
                kind="reclaimed",
                order=1,
                values=reclaimed_values,
                payload_bits=space.payload_bits,
                use_color=use_color,
                limit=args.reserved_limit,
                hidden_counts=hidden_counts,
            )
        if needle is None or needle in "reserved":
            render_synthetic_cubes(
                rows,
                kind="reserved",
                order=2,
                values=reserved_values,
                payload_bits=space.payload_bits,
                use_color=use_color,
                limit=args.reserved_limit,
                hidden_counts=hidden_counts,
            )

    if args.show_reserved:
        rows.sort(key=lambda item: (item[0], item[1], item[2][0]))
    table_rows = [row for _base, _kind, row in rows]
    headers = ["id", "bits", "pattern", "slots" if args.show_reserved else "assigned", "reclaimed", "text"]
    print(format_table(headers, table_rows))
    for kind, count in sorted(hidden_counts.items()):
        print(f"\n... {count:,} more {kind} blocks hidden by --reserved-limit")
    return 0


def patterns_overlap(left: str, right: str) -> bool:
    if len(left) != len(right):
        raise ValueError("patterns must have the same width")
    for a, b in zip(left, right):
        if a in "01" and b in "01" and a != b:
            return False
    return True


def command_check(args: argparse.Namespace) -> int:
    space = load_store_space(args.defs_root, args.cls)
    pattern = normalize_pattern(args.pattern, space.payload_bits)
    shown_pattern = display_pattern(args.pattern, space.payload_bits)
    shown_fields = infer_fields(shown_pattern)
    use_color = color_enabled(args)
    slots = pattern_cardinality(pattern)
    if slots > args.max_expand:
        raise ValueError(f"candidate expands to {slots:,} slots; pass --max-expand above that to check it")

    outside = 0
    clean_free = 0
    reclaimed = Counter()
    collisions = Counter()
    collision_examples: dict[str, str] = {}
    reclaimed_examples: dict[str, str] = {}
    ignored = set(args.ignore_entry or [])

    for value in iter_pattern_values(pattern):
        if not any(matches_pattern(value, namespace) for namespace in space.namespaces):
            outside += 1
            continue
        claim = space.claimed.get(value)
        if claim is not None:
            if claim.entry_id in ignored:
                clean_free += 1
                continue
            key = claim.entry_id
            collisions[key] += 1
            collision_examples.setdefault(key, claim.text)
            continue
        skipped = space.skipped.get(value)
        if skipped:
            skipped = [item for item in skipped if item.entry_id not in ignored]
        if skipped:
            for item in skipped:
                key = f"{item.entry_id}:{item.reason}"
                reclaimed[key] += 1
                reclaimed_examples.setdefault(key, item.text)
            continue
        clean_free += 1

    print(f"class:       {space.cls}")
    print(f"pattern:     {colorize_bits(shown_pattern, shown_fields, use_color)}")
    if shown_pattern != pattern:
        print(f"normalized:  {pattern}")
    print(f"slots:       {slots:,}")
    print(f"clean-free:  {clean_free:,}")
    print(f"reclaimed:   {sum(reclaimed.values()):,}")
    print(f"collisions:  {sum(collisions.values()):,}")
    print(f"outside:     {outside:,}")

    if reclaimed:
        rows = [
            [key, f"{count:,}", reclaimed_examples.get(key, "")]
            for key, count in reclaimed.most_common(args.limit)
        ]
        print("\nreclaimed overlaps")
        print(format_table(["entry:reason", "slots", "text"], rows))
    if collisions:
        rows = [
            [key, f"{count:,}", collision_examples.get(key, "")]
            for key, count in collisions.most_common(args.limit)
        ]
        print("\nclaimed collisions")
        print(format_table(["entry", "slots", "text"], rows))
    return 1 if outside or collisions else 0


def command_holes(args: argparse.Namespace) -> int:
    space = load_store_space(args.defs_root, args.cls)
    all_values = namespace_values(space, args.max_enumerate)
    leading = normalize_pattern(args.leading, space.payload_bits) if args.leading else None

    unavailable = set(space.claimed)
    if not args.include_reclaimed:
        unavailable.update(space.skipped)
    available = all_values - unavailable
    if leading:
        available = {value for value in available if matches_pattern(value, leading)}

    blocks = [
        cube
        for cube in minimized_cubes_from_values(available, space.payload_bits)
        if cube.slots >= args.min_slots
        and (args.max_slots is None or cube.slots <= args.max_slots)
        and cube_pattern(cube).count("?") >= args.min_wildcards
    ]

    if args.sort == "size":
        blocks.sort(key=lambda item: (-item.slots, cube_min_value(item), cube_pattern(item)))
    else:
        blocks.sort(key=lambda item: (cube_min_value(item), -item.slots, cube_pattern(item)))

    rows = [
        [
            cube_pattern(cube),
            f"{cube.slots:,}",
            str(cube_pattern(cube).count("?")),
            cube_span_text(cube),
        ]
        for cube in blocks[: args.limit]
    ]
    print(format_table(["bits", "slots", "wildcards", "span"], rows))
    if len(blocks) > args.limit:
        print(f"\n... {len(blocks) - args.limit:,} more blocks hidden by --limit")
    return 0


def canonical_encodings_yaml(data: dict[str, Any]) -> str:
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        width=1000,
    )


def locate_encoding_form(defs_root: Path, form_id: str) -> tuple[Path, dict[str, Any], int]:
    matches: list[tuple[Path, dict[str, Any], int]] = []
    for path in sorted(defs_root.glob("**/instructions/*/encodings.yaml")):
        data = load_yaml(path)
        for index, form in enumerate(data.get("forms") or []):
            if isinstance(form, dict) and form.get("id") == form_id:
                matches.append((path, data, index))
    if not matches:
        raise ValueError(f"encoding form {form_id!r} not found")
    if len(matches) != 1:
        raise ValueError(f"encoding form {form_id!r} is not globally unique")
    return matches[0]


def instruction_encoding_path(defs_root: Path, mnemonic: str) -> Path:
    matches = [
        path
        for path in defs_root.glob("**/instructions/*/encodings.yaml")
        if path.parent.name == mnemonic
    ]
    if len(matches) != 1:
        raise ValueError(
            f"expected one encoding document for {mnemonic!r}, found {len(matches)}"
        )
    return matches[0]


def decode_form_snippet(path: Path) -> dict[str, Any]:
    from defs_schema import decode_encodings
    from encoding_store import encoding_form_dict

    raw = load_yaml(path)
    if "forms" in raw:
        forms = raw["forms"]
    else:
        forms = [raw]
    if not isinstance(forms, list) or len(forms) != 1:
        raise ValueError(f"{path}: expected exactly one encoding form")
    document = decode_encodings(path, {"forms": forms})
    return encoding_form_dict(document.forms[0])


def constraints_snippet(path: Path) -> list[dict[str, Any]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict) and "constraints" in raw:
        raw = raw["constraints"]
    if not isinstance(raw, list):
        raise ValueError(f"{path}: expected a constraints list")
    if not all(isinstance(item, dict) for item in raw):
        raise ValueError(f"{path}: every constraint must be a mapping")
    return [dict(item) for item in raw]


def validate_candidate_document(
    defs_root: Path,
    target_path: Path,
    candidate: dict[str, Any],
) -> None:
    from defs_loader import load_extensions, load_operand_types, load_size_definitions
    from defs_schema import decode_encodings, decode_instruction
    from encoding_store import LocatedEncoding, allocation_entry_dict, load_encoding_store

    candidate_doc = decode_encodings(target_path, candidate)
    store = load_encoding_store(defs_root)
    class_names = set(store.classes_by_name)
    extensions = load_extensions(defs_root)
    operand_registry = load_operand_types(defs_root, extensions)
    operand_types = set(operand_registry)
    size_codes = set(load_size_definitions(defs_root, extensions)["size_codes"])
    instruction_path = target_path.with_name("instruction.yaml")
    instruction = decode_instruction(instruction_path, load_yaml(instruction_path))
    if instruction.mnemonic != target_path.parent.name:
        raise ValueError(f"{instruction_path}: mnemonic does not match directory")
    for form in candidate_doc.forms:
        if form.encoding_class not in class_names:
            raise ValueError(
                f"{target_path}: form {form.id!r} references unknown class {form.encoding_class!r}"
            )
        syntax_mnemonic = re.split(r"[./(]", form.syntax.split()[0])[0]
        if syntax_mnemonic != instruction.mnemonic:
            raise ValueError(
                f"{target_path}: form {form.id!r} syntax names {syntax_mnemonic}, "
                f"expected {instruction.mnemonic}"
            )
        for operand in form.operands:
            if operand.type not in operand_types:
                raise ValueError(
                    f"{target_path}: form {form.id!r} uses unknown operand type {operand.type!r}"
                )
            elif operand.field is not None:
                expected_width = int(operand_registry[operand.type]["field_width"])
                actual_width = form.bits.count(operand.field)
                if actual_width != expected_width:
                    raise ValueError(
                        f"{target_path}: form {form.id!r} operand {operand.name!r} "
                        f"has {actual_width}-bit field, expected {expected_width}"
                    )
        for marker, field in form.fields.items():
            if field.type != "size" and field.type not in operand_types:
                raise ValueError(
                    f"{target_path}: form {form.id!r} field {marker!r} uses unknown type {field.type!r}"
                )
            if field.type != "size":
                expected_width = int(operand_registry[field.type]["field_width"])
                actual_width = form.bits.count(marker)
                if actual_width != expected_width:
                    raise ValueError(
                        f"{target_path}: form {form.id!r} field {marker!r} "
                        f"has {actual_width} bits, expected {expected_width}"
                    )
        for size in form.sizes:
            if size not in size_codes:
                raise ValueError(f"{target_path}: form {form.id!r} uses unknown size {size!r}")
    target_resolved = target_path.resolve()
    located = [
        item for item in store.encodings if item.path.resolve() != target_resolved
    ]
    located.extend(
        LocatedEncoding(target_path, target_path.parent.name, form)
        for form in candidate_doc.forms
    )

    ids: set[str] = set()
    by_class: dict[str, list[LocatedEncoding]] = defaultdict(list)
    for item in located:
        if item.form.id in ids:
            raise ValueError(f"duplicate encoding id {item.form.id!r}")
        ids.add(item.form.id)
        by_class[item.form.encoding_class].append(item)

    for encoding_class in store.classes:
        claims_by_value: dict[int, Claim] = {}
        for item in by_class.get(encoding_class.name, []):
            entry = allocation_entry_dict(item)
            claims, _skipped = entry_claims(
                item.path,
                encoding_class.payload_bits,
                list(encoding_class.namespace),
                entry,
            )
            for value, claim in claims:
                previous = claims_by_value.get(value)
                if previous is not None:
                    raise ValueError(
                        f"0x{value:x}: {previous.entry_id} overlaps {claim.entry_id}"
                    )
                claims_by_value[value] = claim


def preview_or_apply(
    path: Path,
    data: dict[str, Any],
    *,
    apply: bool,
) -> None:
    before = path.read_text(encoding="utf-8")
    after = canonical_encodings_yaml(data)
    diff = "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=str(path),
            tofile=str(path),
        )
    )
    print(diff or "(no changes)", end="" if diff else "\n")
    if not apply or before == after:
        return
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(after, encoding="utf-8")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def command_add(args: argparse.Namespace) -> int:
    path = instruction_encoding_path(args.defs_root, args.mnemonic)
    data = load_yaml(path)
    form = decode_form_snippet(args.form)
    data.setdefault("forms", []).append(form)
    validate_candidate_document(args.defs_root, path, data)
    preview_or_apply(path, data, apply=args.apply)
    return 0


def command_move(args: argparse.Namespace) -> int:
    path, data, index = locate_encoding_form(args.defs_root, args.form_id)
    form = data["forms"][index]
    if args.cls is not None:
        form["class"] = args.cls
    if args.bits is not None:
        form["bits"] = args.bits
    validate_candidate_document(args.defs_root, path, data)
    preview_or_apply(path, data, apply=args.apply)
    return 0


def command_edit(args: argparse.Namespace) -> int:
    path, data, index = locate_encoding_form(args.defs_root, args.form_id)
    form = data["forms"][index]
    if args.bits is not None:
        form["bits"] = args.bits
    if args.constraints is not None:
        constraints = constraints_snippet(args.constraints)
        if constraints:
            form["constraints"] = constraints
        else:
            form.pop("constraints", None)
    validate_candidate_document(args.defs_root, path, data)
    preview_or_apply(path, data, apply=args.apply)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--defs-root", type=Path, default=DEFAULT_DEFS_ROOT)
    parser.add_argument("--color", choices=["auto", "always", "never"], default="auto")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_color_option(target: argparse.ArgumentParser) -> None:
        target.add_argument("--color", choices=["auto", "always", "never"], default=argparse.SUPPRESS)

    summary = sub.add_parser("summary", help="show class occupancy using claimed and reclaimed slots")
    add_color_option(summary)
    summary.set_defaults(func=command_summary)

    legend = sub.add_parser("legend", help="show field-kind colors")
    add_color_option(legend)
    legend.set_defaults(func=command_legend)

    entries = sub.add_parser("entries", help="list allocation entries, optionally filtered")
    add_color_option(entries)
    entries.add_argument("cls")
    entries.add_argument("--leading", help="0/1/? leading-bit pattern; shorter patterns are padded with ?")
    entries.add_argument("--grep", help="case-insensitive id/text filter")
    entries.add_argument("--show-reserved", action="store_true", help="include computed reserved blocks")
    entries.add_argument("--reserved-limit", type=int, default=0, help="max reserved rows; 0 means no limit")
    entries.add_argument("--max-enumerate", type=int, default=DEFAULT_MAX_ENUMERATE)
    entries.set_defaults(func=command_entries)

    check = sub.add_parser("check", help="check whether a candidate pattern is free")
    add_color_option(check)
    check.add_argument("cls")
    check.add_argument("pattern", help="0/1/? pattern; shorter patterns are padded with ?")
    check.add_argument("--max-expand", type=int, default=1 << 22)
    check.add_argument("--limit", type=int, default=12)
    check.add_argument("--ignore-entry", action="append", help="ignore an existing entry id while checking")
    check.set_defaults(func=command_check)

    holes = sub.add_parser("holes", help="list aligned clean-free blocks")
    add_color_option(holes)
    holes.add_argument("cls")
    holes.add_argument("--leading", help="0/1/? leading-bit pattern; shorter patterns are padded with ?")
    holes.add_argument("--include-reclaimed", action="store_true")
    holes.add_argument("--min-slots", type=int, default=1)
    holes.add_argument("--max-slots", type=int)
    holes.add_argument("--min-wildcards", type=int, default=0)
    holes.add_argument("--limit", type=int, default=32)
    holes.add_argument("--sort", choices=["size", "address"], default="size")
    holes.add_argument("--max-enumerate", type=int, default=DEFAULT_MAX_ENUMERATE)
    holes.set_defaults(func=command_holes)

    add = sub.add_parser("add", help="validate and add one encoding form")
    add.add_argument("mnemonic")
    add.add_argument("form", type=Path, help="YAML file containing one form")
    add.add_argument("--apply", action="store_true", help="atomically apply after validation")
    add.set_defaults(func=command_add)

    move = sub.add_parser("move", help="move an existing form to a class/bit pattern")
    move.add_argument("form_id")
    move.add_argument("--class", dest="cls")
    move.add_argument("--bits")
    move.add_argument("--apply", action="store_true", help="atomically apply after validation")
    move.set_defaults(func=command_move)

    edit = sub.add_parser("edit", help="edit bits and/or constraints of an existing form")
    edit.add_argument("form_id")
    edit.add_argument("--bits")
    edit.add_argument("--constraints", type=Path, help="YAML constraints list")
    edit.add_argument("--apply", action="store_true", help="atomically apply after validation")
    edit.set_defaults(func=command_edit)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except BrokenPipeError:
        return 1
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
