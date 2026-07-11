#!/usr/bin/env python3
"""Generate allocation occupancy reports from hand-authored encoding YAML."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from alloc_notes import allocation_form_text, allocation_note_text
from validate_alloc import (
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


CLASS_INSTRUCTION_BYTES = {
    "extrashort": 1,
    "short": 2,
    "medium": 3,
    "long": 4,
    "extralong": 5,
}

CLASS_ORDER = {
    "extrashort": 0,
    "short": 1,
    "medium": 2,
    "long": 3,
    "extralong": 4,
}


@dataclass(frozen=True)
class EntryReport:
    cls: str
    path: str
    entry_id: str
    mnemonic: str
    bits: str
    pattern_slots: int
    assigned_slots: int
    reclaimed_slots: int
    reclaim_reasons: dict[str, int]
    text: str
    notes: str


@dataclass(frozen=True)
class ClassReport:
    cls: str
    path: str
    payload_bits: int
    instruction_bytes: int | None
    namespace_slots: int
    allocated_slots: int
    claimed_slots: int
    unclaimed_slots: int
    clean_free_slots: int
    remaining_slots: int
    reclaimed_slots: int
    reclaim_reasons: dict[str, int]
    overlaps: list[str]


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping")
    return data


def mnemonic_from_text(text: str, entry_id: str) -> str:
    form = allocation_form_text(text)
    first = form.strip().split(maxsplit=1)[0] if form.strip() else entry_id.rsplit(".", 1)[-1]
    return first


def entry_skipped_values(
    path: Path,
    payload_bits: int,
    namespaces: list[str],
    entry: dict[str, Any],
) -> set[int]:
    entry_id = str(entry["id"])
    pattern = compact_bits(str(entry["bits"]))
    constraints = entry.get("constraints") or []
    if len(pattern) != payload_bits:
        raise ValueError(f"{entry_id}: pattern has {len(pattern)} bits, expected {payload_bits}")

    out: set[int] = set()
    for value in expand_pattern(pattern):
        if not any(matches_pattern(value, namespace) for namespace in namespaces):
            raise ValueError(f"{entry_id}: value 0x{value:x} is outside class namespace")

        for constraint in constraints:
            if "allow" in constraint and not field_allowed(value, pattern, constraint):
                out.add(value)
                break
            if "exclude" in constraint and excluded_by(value, pattern, constraint):
                out.add(value)
                break
    return out


def analyze_file(path: Path) -> tuple[ClassReport, list[EntryReport]]:
    data = load_yaml(path)
    if "escapes" in data:
        raise ValueError(f"{path}: top-level escapes are no longer supported; use class namespace patterns")
    cls = str(data["class"])
    payload_bits = int(data["payload_bits"])
    namespaces = namespace_patterns(payload_bits, data)
    total_slots = namespace_size(namespaces)

    by_value: dict[int, Claim] = {}
    overlaps: list[str] = []
    class_skipped: Counter[str] = Counter()
    allocated_values: set[int] = set()
    skipped_values: set[int] = set()
    entry_reports: list[EntryReport] = []

    for entry in data.get("entries") or []:
        pattern = compact_bits(str(entry["bits"]))
        text = allocation_form_text(str(entry.get("text", "")))
        claims, skipped = entry_claims(path, payload_bits, namespaces, entry)
        class_skipped.update(skipped)
        skipped_values.update(entry_skipped_values(path, payload_bits, namespaces, entry))

        entry_reports.append(
            EntryReport(
                cls=cls,
                path=str(path),
                entry_id=str(entry["id"]),
                mnemonic=mnemonic_from_text(text, str(entry["id"])),
                bits=pattern,
                pattern_slots=pattern_cardinality(pattern),
                assigned_slots=len(claims),
                reclaimed_slots=sum(skipped.values()),
                reclaim_reasons=dict(sorted(skipped.items())),
                text=text,
                notes=allocation_note_text(entry),
            )
        )

        for value, claim in claims:
            previous = by_value.get(value)
            if previous is not None:
                overlaps.append(f"0x{value:x}: {previous.entry_id} overlaps {claim.entry_id}")
                continue
            by_value[value] = claim
            allocated_values.add(value)

    allocated_slots = len(allocated_values)
    claimed_slots = len(by_value)
    unclaimed_slots = total_slots - claimed_slots
    clean_free_slots = total_slots - len(allocated_values | skipped_values)

    return (
        ClassReport(
            cls=cls,
            path=str(path),
            payload_bits=payload_bits,
            instruction_bytes=CLASS_INSTRUCTION_BYTES.get(cls),
            namespace_slots=total_slots,
            allocated_slots=allocated_slots,
            claimed_slots=claimed_slots,
            unclaimed_slots=unclaimed_slots,
            clean_free_slots=clean_free_slots,
            remaining_slots=total_slots - allocated_slots,
            reclaimed_slots=sum(class_skipped.values()),
            reclaim_reasons=dict(sorted(class_skipped.items())),
            overlaps=overlaps,
        ),
        entry_reports,
    )


def analyze(paths: list[Path]) -> tuple[list[ClassReport], list[EntryReport]]:
    class_reports: list[ClassReport] = []
    entry_reports: list[EntryReport] = []
    for path in sorted(paths, key=lambda p: (CLASS_ORDER.get(p.stem, 99), str(p))):
        class_report, entries = analyze_file(path)
        class_reports.append(class_report)
        entry_reports.extend(entries)
    return class_reports, entry_reports


def int_text(value: int) -> str:
    return f"{value:,}"


def percent(part: int, whole: int) -> str:
    if whole == 0:
        return "-"
    return f"{part / whole * 100:.4f}%"


def reason_text(reasons: dict[str, int]) -> str:
    if not reasons:
        return "-"
    return ", ".join(f"{key}={int_text(value)}" for key, value in reasons.items())


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "_No entries._\n"
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in rows))
        for index in range(len(headers))
    ]
    out = [
        "| " + " | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)) + " |",
        "| " + " | ".join("-" * widths[index] for index in range(len(headers))) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(cell.ljust(widths[index]) for index, cell in enumerate(row)) + " |")
    return "\n".join(out) + "\n"


def mnemonic_totals(entries: list[EntryReport]) -> list[dict[str, Any]]:
    totals: dict[tuple[str, str], dict[str, Any]] = {}
    for entry in entries:
        key = (entry.cls, entry.mnemonic)
        item = totals.setdefault(
            key,
            {
                "class": entry.cls,
                "mnemonic": entry.mnemonic,
                "forms": 0,
                "allocated_slots": 0,
                "reclaimed_slots": 0,
            },
        )
        item["forms"] += 1
        item["allocated_slots"] += entry.assigned_slots
        item["reclaimed_slots"] += entry.reclaimed_slots

    return sorted(
        totals.values(),
        key=lambda item: (CLASS_ORDER.get(str(item["class"]), 99), -int(item["allocated_slots"]), str(item["mnemonic"])),
    )


def render_markdown(classes: list[ClassReport], entries: list[EntryReport]) -> str:
    lines = [
        "# Encoding Allocation Report",
        "",
        "Generated from `isa/alloc/*.yaml`. Slot counts are opcode payload slots inside each allocation namespace.",
        "`reclaimed` counts are slots excluded by entry constraints before assignment. `remaining` is namespace slots minus allocated instruction slots. `clean-free` excludes both allocated and reclaimed slots.",
        "",
        "## Class Summary",
        "",
    ]
    lines.append(
        markdown_table(
            [
                "Class",
                "Bytes",
                "Payload bits",
                "Namespace",
                "Allocated",
                "Allocated %",
                "Unclaimed",
                "Clean-free",
                "Remaining",
                "Reclaimed",
                "Overlaps",
            ],
            [
                [
                    item.cls,
                    str(item.instruction_bytes or "-"),
                    str(item.payload_bits),
                    int_text(item.namespace_slots),
                    int_text(item.allocated_slots),
                    percent(item.allocated_slots, item.namespace_slots),
                    int_text(item.unclaimed_slots),
                    int_text(item.clean_free_slots),
                    int_text(item.remaining_slots),
                    int_text(item.reclaimed_slots),
                    str(len(item.overlaps)),
                ]
                for item in classes
            ],
        )
    )

    lines.extend(["", "## Reclaim Reasons", ""])
    reason_rows: list[list[str]] = []
    for item in classes:
        if not item.reclaim_reasons:
            reason_rows.append([item.cls, "-", "0"])
            continue
        for reason, count in item.reclaim_reasons.items():
            reason_rows.append([item.cls, reason, int_text(count)])
    lines.append(markdown_table(["Class", "Reason", "Slots"], reason_rows))

    lines.extend(["", "## Instruction Totals", ""])
    lines.append(
        markdown_table(
            ["Class", "Mnemonic", "Forms", "Allocated", "Reclaimed"],
            [
                [
                    str(item["class"]),
                    str(item["mnemonic"]),
                    int_text(int(item["forms"])),
                    int_text(int(item["allocated_slots"])),
                    int_text(int(item["reclaimed_slots"])),
                ]
                for item in mnemonic_totals(entries)
            ],
        )
    )

    lines.extend(["", "## Form Detail", ""])
    for cls in sorted({entry.cls for entry in entries}, key=lambda name: CLASS_ORDER.get(name, 99)):
        lines.extend(["", f"### {cls}", ""])
        cls_entries = [entry for entry in entries if entry.cls == cls]
        lines.append(
            markdown_table(
                ["ID", "Pattern slots", "Assigned", "Reclaimed", "Reclaim reasons", "Bits", "Form", "Notes"],
                [
                    [
                        entry.entry_id,
                        int_text(entry.pattern_slots),
                        int_text(entry.assigned_slots),
                        int_text(entry.reclaimed_slots),
                        reason_text(entry.reclaim_reasons),
                        f"`{entry.bits}`",
                        entry.text,
                        entry.notes,
                    ]
                    for entry in cls_entries
                ],
            )
        )

    overlap_items = [(item.cls, overlap) for item in classes for overlap in item.overlaps]
    if overlap_items:
        lines.extend(["", "## Overlaps", ""])
        lines.append(markdown_table(["Class", "Overlap"], [[cls, overlap] for cls, overlap in overlap_items]))

    return "\n".join(lines).rstrip() + "\n"


def write_csv(path: Path, headers: list[str], rows: list[list[Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def write_outputs(
    out_dir: Path,
    base_name: str,
    classes: list[ClassReport],
    entries: list[EntryReport],
) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "markdown": out_dir / f"{base_name}.md",
        "json": out_dir / f"{base_name}.json",
        "classes_csv": out_dir / f"{base_name}_classes.csv",
        "entries_csv": out_dir / f"{base_name}_entries.csv",
        "mnemonics_csv": out_dir / f"{base_name}_mnemonics.csv",
    }

    paths["markdown"].write_text(render_markdown(classes, entries), encoding="utf-8")

    payload = {
        "classes": [item.__dict__ for item in classes],
        "entries": [item.__dict__ for item in entries],
        "mnemonics": mnemonic_totals(entries),
    }
    paths["json"].write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    write_csv(
        paths["classes_csv"],
        [
            "class",
            "path",
            "payload_bits",
            "instruction_bytes",
            "namespace_slots",
            "allocated_slots",
            "claimed_slots",
            "unclaimed_slots",
            "clean_free_slots",
            "remaining_slots",
            "reclaimed_slots",
            "reclaim_reasons",
            "overlap_count",
        ],
        [
            [
                item.cls,
                item.path,
                item.payload_bits,
                item.instruction_bytes or "",
                item.namespace_slots,
                item.allocated_slots,
                item.claimed_slots,
                item.unclaimed_slots,
                item.clean_free_slots,
                item.remaining_slots,
                item.reclaimed_slots,
                reason_text(item.reclaim_reasons),
                len(item.overlaps),
            ]
            for item in classes
        ],
    )
    write_csv(
        paths["entries_csv"],
        [
            "class",
            "id",
            "mnemonic",
            "bits",
            "pattern_slots",
            "assigned_slots",
            "reclaimed_slots",
            "reclaim_reasons",
            "form",
            "notes",
        ],
        [
            [
                entry.cls,
                entry.entry_id,
                entry.mnemonic,
                entry.bits,
                entry.pattern_slots,
                entry.assigned_slots,
                entry.reclaimed_slots,
                reason_text(entry.reclaim_reasons),
                entry.text,
                entry.notes,
            ]
            for entry in entries
        ],
    )
    write_csv(
        paths["mnemonics_csv"],
        ["class", "mnemonic", "forms", "allocated_slots", "reclaimed_slots"],
        [
            [
                item["class"],
                item["mnemonic"],
                item["forms"],
                item["allocated_slots"],
                item["reclaimed_slots"],
            ]
            for item in mnemonic_totals(entries)
        ],
    )

    return list(paths.values())


def default_paths() -> list[Path]:
    return sorted(Path("isa/alloc").glob("*.yaml"), key=lambda p: (CLASS_ORDER.get(p.stem, 99), str(p)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, default=default_paths())
    parser.add_argument("--out-dir", type=Path, default=Path("build/reports"))
    parser.add_argument("--base-name", default="encoding_allocation_report")
    args = parser.parse_args()

    classes, entries = analyze(args.paths)
    written = write_outputs(args.out_dir, args.base_name, classes, entries)

    for item in classes:
        print(
            f"{item.cls}: allocated={item.allocated_slots} "
            f"reclaimed={item.reclaimed_slots} clean_free={item.clean_free_slots} "
            f"remaining={item.remaining_slots} "
            f"namespace={item.namespace_slots}"
        )
    for path in written:
        print(path)

    return 1 if any(item.overlaps for item in classes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
