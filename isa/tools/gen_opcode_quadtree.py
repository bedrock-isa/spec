#!/usr/bin/env python3
"""Render current opcode allocations as an interactive quadtree HTML file."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from encoding_store import EncodingStore, class_entries, load_encoding_store
from validate_alloc import compact_bits, parse_range


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DEFS_ROOT = REPOSITORY_ROOT / "isa" / "instructions" / "definitions"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "build" / "reports" / "opcode_quadtree.html"
MAX_DEPTH = 7


@dataclass(frozen=True)
class PrefixCell:
    prefix: str
    namespace_slots: int
    allocated_slots: int
    entries: tuple[dict[str, Any], ...]


def _field_positions(pattern: str) -> dict[str, list[int]]:
    positions: dict[str, list[int]] = {}
    for index, char in enumerate(pattern):
        if char not in "01?":
            positions.setdefault(char, []).append(index)
    return positions


def _prefix_allows_value(
    value: int,
    positions: list[int],
    prefix: str,
) -> bool:
    width = len(positions)
    for field_index, pattern_index in enumerate(positions):
        if pattern_index >= len(prefix):
            continue
        bit = (value >> (width - field_index - 1)) & 1
        if bit != int(prefix[pattern_index]):
            return False
    return True


def _constraint_allows_value(
    value: int,
    constraints: Iterable[dict[str, Any]],
) -> bool:
    for constraint in constraints:
        if "allow" in constraint:
            ranges = [parse_range(item) for item in constraint["allow"]]
            if not any(low <= value <= high for low, high in ranges):
                return False
        if constraint.get("exclude") == "immediate" and 0x5B <= value <= 0x5E:
            return False
        if "exclude" in constraint and constraint["exclude"] != "immediate":
            raise ValueError(f"unknown exclude predicate {constraint['exclude']!r}")
    return True


def count_entry_in_prefix(entry: dict[str, Any], prefix: str) -> int:
    """Count exactly how many values from an entry lie below a binary prefix."""
    pattern = compact_bits(str(entry["bits"]))
    if len(prefix) > len(pattern) or set(prefix) - {"0", "1"}:
        raise ValueError(f"invalid {len(prefix)}-bit prefix for {len(pattern)}-bit pattern")

    for index, bit in enumerate(prefix):
        if pattern[index] in "01" and pattern[index] != bit:
            return 0

    field_positions = _field_positions(pattern)
    constraints_by_field: dict[str, list[dict[str, Any]]] = {}
    for constraint in entry.get("constraints") or []:
        field = str(constraint["field"])
        if field not in field_positions:
            raise ValueError(
                f"{entry.get('id', '<entry>')}: constraint references missing field {field!r}"
            )
        constraints_by_field.setdefault(field, []).append(constraint)

    count = 1
    for field, positions in field_positions.items():
        allowed = sum(
            1
            for value in range(1 << len(positions))
            if _prefix_allows_value(value, positions, prefix)
            and _constraint_allows_value(value, constraints_by_field.get(field, ()))
        )
        count *= allowed
        if count == 0:
            return 0

    unfixed_wildcards = sum(
        1 for index, char in enumerate(pattern) if char == "?" and index >= len(prefix)
    )
    return count << unfixed_wildcards


def count_pattern_in_prefix(pattern: str, prefix: str) -> int:
    """Count values shared by a 0/1/? pattern and a concrete prefix."""
    pattern = compact_bits(pattern)
    if len(prefix) > len(pattern):
        raise ValueError("prefix is wider than pattern")
    for index, bit in enumerate(prefix):
        if pattern[index] in "01" and pattern[index] != bit:
            return 0
    return 1 << sum(
        1 for index, char in enumerate(pattern) if char == "?" and index >= len(prefix)
    )


def binary_prefixes(width: int) -> Iterable[str]:
    if width == 0:
        yield ""
        return
    for value in range(1 << width):
        yield f"{value:0{width}b}"


def namespace_root_prefix(patterns: Iterable[str]) -> str:
    """Return the concrete prefix shared by every namespace pattern."""
    compact = [compact_bits(pattern) for pattern in patterns]
    if not compact:
        return ""
    out: list[str] = []
    for chars in zip(*compact):
        if len(set(chars)) != 1 or chars[0] not in "01":
            break
        out.append(chars[0])
    return "".join(out)


def build_class_view(
    store: EncodingStore,
    class_name: str,
    depth: int,
) -> dict[str, Any]:
    encoding_class = store.classes_by_name[class_name]
    entries = class_entries(store, class_name)
    root_prefix = namespace_root_prefix(encoding_class.namespace)
    relative_width = min(
        encoding_class.allocation_bits - len(root_prefix),
        depth * 2,
    )
    prefix_width = len(root_prefix) + relative_width
    cells: list[PrefixCell] = []
    boundaries: list[str] = []

    def cell_for_prefix(prefix: str) -> PrefixCell | None:
        namespace_slots = sum(
            count_pattern_in_prefix(pattern, prefix)
            for pattern in encoding_class.namespace
        )
        if namespace_slots == 0:
            return None

        assigned: list[dict[str, Any]] = []
        allocated_slots = 0
        for entry in entries:
            slots = count_entry_in_prefix(entry, prefix)
            if slots == 0:
                continue
            allocated_slots += slots
            entry_id = str(entry["id"])
            assigned.append(
                {
                    "id": entry_id,
                    "mnemonic": str(entry["mnemonic"]),
                    "syntax": str(entry["syntax"]),
                    "slots": slots,
                }
            )

        if allocated_slots > namespace_slots:
            raise ValueError(
                f"{class_name} prefix {prefix}: allocations exceed namespace; "
                "validate opcode overlaps"
            )
        assigned.sort(key=lambda item: (-int(item["slots"]), str(item["id"])))
        return PrefixCell(
            prefix,
            namespace_slots,
            allocated_slots,
            tuple(assigned),
        )

    def visit(prefix: str, level: int) -> None:
        cell = cell_for_prefix(prefix)
        if cell is None:
            return
        remaining_bits = encoding_class.allocation_bits - len(prefix)
        homogeneous_assignment = (
            cell.allocated_slots == cell.namespace_slots
            and len(cell.entries) == 1
            and int(cell.entries[0]["slots"]) == cell.namespace_slots
        )
        terminal = (
            level >= depth
            or remaining_bits == 0
            or cell.allocated_slots == 0
            or homogeneous_assignment
        )
        if terminal:
            cells.append(cell)
            return

        boundaries.append(prefix[len(root_prefix) :])
        child_width = min(2, remaining_bits)
        for suffix in binary_prefixes(child_width):
            visit(prefix + suffix, level + 1)

    visit(root_prefix, 0)

    namespace_slots = sum(1 << pattern.count("?") for pattern in encoding_class.namespace)
    total_allocated = sum(cell.allocated_slots for cell in cells)
    return {
        "name": class_name,
        "allocationBits": encoding_class.allocation_bits,
        "opcodeBytes": encoding_class.opcode_space_bytes,
        "prefixWidth": prefix_width,
        "rootPrefix": root_prefix,
        "depth": math.ceil(relative_width / 2),
        "namespaceSlots": namespace_slots,
        "allocatedSlots": total_allocated,
        "forms": len(entries),
        "boundaries": boundaries,
        "cells": [
            {
                "prefix": cell.prefix,
                "layoutPrefix": cell.prefix[len(root_prefix) :],
                "level": math.ceil((len(cell.prefix) - len(root_prefix)) / 2),
                "namespaceSlots": cell.namespace_slots,
                "allocatedSlots": cell.allocated_slots,
                "entries": list(cell.entries),
            }
            for cell in cells
        ],
    }


def build_payload(
    store: EncodingStore,
    selected_classes: Iterable[str],
    depth: int,
) -> dict[str, Any]:
    resolved_defs = store.defs_root.resolve()
    try:
        source = str(resolved_defs.relative_to(REPOSITORY_ROOT))
    except ValueError:
        source = f"external definitions ({resolved_defs.name})"
    return {
        "classes": [build_class_view(store, name, depth) for name in selected_classes],
        "source": source,
    }


def _safe_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def render_html(payload: dict[str, Any]) -> str:
    data = _safe_json(payload)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bedrock ISA opcode quadtree</title>
<style>
:root {{ color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #09111f; color: #e7eefb; }}
main {{ max-width: 1440px; margin: auto; padding: 28px; }}
header {{ display: flex; justify-content: space-between; gap: 24px; align-items: end; margin-bottom: 18px; }}
h1 {{ margin: 0 0 6px; font-size: clamp(24px, 3vw, 38px); letter-spacing: -0.035em; }}
.subtitle {{ margin: 0; color: #8fa4c3; }}
.tabs {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0; }}
button {{ border: 1px solid #263653; color: #aebdd3; background: #111c2e; border-radius: 999px; padding: 8px 13px; cursor: pointer; }}
button.active {{ color: #06111c; background: #73e0c1; border-color: #73e0c1; font-weight: 700; }}
.stats {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-bottom: 16px; }}
.stat {{ padding: 13px 15px; background: #101b2c; border: 1px solid #1e304b; border-radius: 12px; }}
.stat span {{ display: block; color: #8298b8; font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }}
.stat strong {{ display: block; margin-top: 4px; font-size: 19px; }}
.workspace {{ display: grid; grid-template-columns: minmax(420px, 1fr) minmax(280px, 380px); gap: 16px; align-items: start; }}
.panel {{ background: #0e192a; border: 1px solid #1e304b; border-radius: 14px; overflow: hidden; }}
.map-wrap {{ padding: 12px; aspect-ratio: 1; }}
svg {{ width: 100%; height: 100%; display: block; background: #07101e; border-radius: 8px; }}
.cell {{ stroke: #09111f; vector-effect: non-scaling-stroke; cursor: crosshair; transition: filter .1s; }}
.cell:hover, .cell.selected {{ stroke: #fff; filter: brightness(1.25); }}
.branch {{ fill: none; stroke: #91a8c9; stroke-opacity: .42; pointer-events: none; vector-effect: non-scaling-stroke; }}
.details {{ padding: 18px; min-height: 420px; }}
.details h2 {{ margin: 0 0 6px; font-size: 18px; overflow-wrap: anywhere; }}
.details .hint {{ color: #8fa4c3; line-height: 1.5; }}
.meter {{ height: 8px; background: #1b2a40; border-radius: 99px; overflow: hidden; margin: 14px 0 8px; }}
.meter div {{ height: 100%; background: #73e0c1; }}
.entry-list {{ list-style: none; padding: 0; margin: 16px 0 0; max-height: 520px; overflow: auto; }}
.entry-list li {{ padding: 10px 0; border-top: 1px solid #1c2b42; }}
.entry-list code {{ color: #8de8ce; font-size: 12px; overflow-wrap: anywhere; }}
.entry-list small {{ display: block; color: #8fa4c3; margin-top: 4px; }}
.legend {{ display: flex; align-items: center; gap: 10px; color: #8fa4c3; font-size: 12px; margin-top: 12px; }}
.gradient {{ width: 180px; height: 9px; border-radius: 99px; background: linear-gradient(90deg, #17253a, #1d6871, #55d6b2); }}
footer {{ color: #7186a3; font-size: 12px; margin-top: 14px; }}
@media (max-width: 850px) {{ .workspace {{ grid-template-columns: 1fr; }} .stats {{ grid-template-columns: repeat(2, 1fr); }} header {{ align-items: start; flex-direction: column; }} }}
</style>
</head>
<body>
<main>
  <header><div><h1>Opcode allocation quadtree</h1><p class="subtitle">Up to two opcode bits per spatial subdivision; hover or click a cell to inspect its prefix.</p></div></header>
  <nav class="tabs" id="tabs" aria-label="Encoding class"></nav>
  <section class="stats" id="stats"></section>
  <section class="workspace">
    <div class="panel"><div class="map-wrap"><svg id="map" viewBox="0 0 1024 1024" role="img" aria-label="Opcode allocation quadtree"></svg></div></div>
    <aside class="panel details" id="details"><p class="hint">Choose a cell to see the allocated forms in that opcode prefix.</p></aside>
  </section>
  <div class="legend"><span>free</span><div class="gradient"></div><span>fully allocated</span></div>
  <footer id="source"></footer>
</main>
<script>
const DATA = {data};
const NS = "http://www.w3.org/2000/svg";
const tabs = document.getElementById("tabs");
const stats = document.getElementById("stats");
const map = document.getElementById("map");
const details = document.getElementById("details");
document.getElementById("source").textContent = `Source: ${{DATA.source}}`;
let active = 0;
let selected = null;
const fmt = value => new Intl.NumberFormat().format(value);
function layout(prefix) {{
  let x = 0, y = 0, width = 1024, height = 1024;
  for (let i = 0; i < prefix.length; i += 2) {{
    const pair = prefix.slice(i, i + 2);
    if (pair.length === 1) {{ width /= 2; if (pair === "1") x += width; continue; }}
    width /= 2; height /= 2;
    const quadrant = parseInt(pair, 2);
    if (quadrant & 1) x += width;
    if (quadrant & 2) y += height;
  }}
  return [x, y, width, height];
}}
function color(ratio) {{
  if (ratio <= 0) return "#17253a";
  const t = Math.sqrt(ratio);
  const a = [29, 73, 84], b = [85, 214, 178];
  return `rgb(${{a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(",")}})`;
}}
const esc = value => String(value).replace(/[&<>"']/g, char => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[char]));
function showDetails(cell, cls) {{
  const ratio = cell.allocatedSlots / cell.namespaceSlots;
  const pattern = cell.prefix + "?".repeat(cls.allocationBits - cell.prefix.length);
  details.innerHTML = `<h2><code>${{esc(pattern)}}</code></h2>
    <p class="hint">${{cell.prefix.length}}-bit prefix · ${{fmt(cell.namespaceSlots)}} namespace slots</p>
    <div class="meter"><div style="width:${{ratio * 100}}%"></div></div>
    <p><strong>${{fmt(cell.allocatedSlots)}}</strong> allocated · <strong>${{fmt(cell.namespaceSlots - cell.allocatedSlots)}}</strong> free · ${{(ratio * 100).toFixed(2)}}%</p>
    <ul class="entry-list">${{cell.entries.length ? cell.entries.map(entry => `<li><code>${{esc(entry.id)}}</code><small>${{esc(entry.syntax)}} · ${{fmt(entry.slots)}} slots</small></li>`).join("") : "<li><span class='hint'>No assigned forms in this prefix.</span></li>"}}</ul>`;
}}
function render(index) {{
  active = index; selected = null;
  const cls = DATA.classes[index];
  [...tabs.children].forEach((button, i) => button.classList.toggle("active", i === index));
  const ratio = cls.allocatedSlots / cls.namespaceSlots;
  stats.innerHTML = [
    ["class", esc(cls.name)], ["opcode space", `${{cls.opcodeBytes}} bytes / ${{cls.allocationBits}} bits`],
    ["allocated", `${{fmt(cls.allocatedSlots)}} · ${{(ratio * 100).toFixed(2)}}%`], ["forms", fmt(cls.forms)]
  ].map(([label, value]) => `<div class="stat"><span>${{label}}</span><strong>${{value}}</strong></div>`).join("");
  map.replaceChildren();
  for (const cell of cls.cells) {{
    const [x, y, width, height] = layout(cell.layoutPrefix);
    const rect = document.createElementNS(NS, "rect");
    const gap = Math.max(0.8, 4 - cell.level * .38);
    rect.setAttribute("x", x + gap / 2); rect.setAttribute("y", y + gap / 2);
    rect.setAttribute("width", Math.max(0, width - gap)); rect.setAttribute("height", Math.max(0, height - gap));
    rect.setAttribute("rx", Math.max(0, 4 - cls.depth * .4));
    rect.setAttribute("fill", color(cell.allocatedSlots / cell.namespaceSlots));
    rect.setAttribute("class", "cell");
    rect.setAttribute("tabindex", "0");
    rect.setAttribute("aria-label", `prefix ${{cell.prefix}}, ${{cell.allocatedSlots}} of ${{cell.namespaceSlots}} allocated`);
    const choose = () => {{ if (selected) selected.classList.remove("selected"); selected = rect; rect.classList.add("selected"); showDetails(cell, cls); }};
    rect.addEventListener("mouseenter", () => showDetails(cell, cls));
    rect.addEventListener("click", choose); rect.addEventListener("focus", choose);
    map.appendChild(rect);
  }}
  for (const prefix of cls.boundaries) {{
    const [x, y, width, height] = layout(prefix);
    const rect = document.createElementNS(NS, "rect");
    rect.setAttribute("x", x + .6); rect.setAttribute("y", y + .6);
    rect.setAttribute("width", Math.max(0, width - 1.2)); rect.setAttribute("height", Math.max(0, height - 1.2));
    rect.setAttribute("class", "branch");
    rect.setAttribute("stroke-width", Math.max(.8, 2.6 - prefix.length * .08));
    map.appendChild(rect);
  }}
  const root = cls.rootPrefix ? ` The view is zoomed to namespace root <code>${{esc(cls.rootPrefix)}}</code>.` : "";
  details.innerHTML = `<p class="hint">Hover or click one of the ${{fmt(cls.cells.length)}} adaptive leaves. Mixed regions subdivide by up to two opcode bits; free and single-form regions stay large.${{root}}</p>`;
}}
DATA.classes.forEach((cls, index) => {{
  const button = document.createElement("button"); button.textContent = cls.name;
  button.addEventListener("click", () => render(index)); tabs.appendChild(button);
}});
render(0);
</script>
</body>
</html>
"""


def class_name(value: str) -> str:
    if value == "all":
        return value
    valid = {"extrashort", "short", "medium", "long", "extralong"}
    if value not in valid:
        raise argparse.ArgumentTypeError(f"must be 'all' or one of {', '.join(sorted(valid))}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--defs", type=Path, default=DEFAULT_DEFS_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--class", dest="class_", type=class_name, default="all")
    parser.add_argument(
        "--depth",
        type=int,
        choices=range(1, MAX_DEPTH + 1),
        default=5,
        metavar="1..7",
        help="quadtree depth; each level consumes two opcode bits (default: 5)",
    )
    args = parser.parse_args()

    store = load_encoding_store(args.defs)
    selected = (
        [encoding_class.name for encoding_class in store.classes]
        if args.class_ == "all"
        else [args.class_]
    )
    payload = build_payload(store, selected, args.depth)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_html(payload), encoding="utf-8")
    for item in payload["classes"]:
        print(
            f"{item['name']}: allocated={item['allocatedSlots']:,} / "
            f"{item['namespaceSlots']:,} ({item['allocatedSlots'] / item['namespaceSlots']:.2%})"
        )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
