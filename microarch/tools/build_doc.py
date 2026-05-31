#!/usr/bin/env python3
"""Concatenate ordered microarchitecture source fragments."""

from __future__ import annotations

import argparse
from pathlib import Path


def manifest_entries(path: Path) -> list[str]:
    entries: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        entries.append(stripped)
    return entries


def build(manifest: Path, src_dir: Path, output: Path) -> None:
    chunks = [
        "<!-- Generated from microarch/src. Edit source fragments, not this file. -->",
        "",
    ]
    for entry in manifest_entries(manifest):
        source = src_dir / entry
        if not source.exists():
            raise FileNotFoundError(source)
        text = source.read_text(encoding="utf-8").strip()
        chunks.append(text)
        chunks.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {output}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--src-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    build(Path(args.manifest), Path(args.src_dir), Path(args.output))


if __name__ == "__main__":
    main()
