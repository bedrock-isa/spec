#!/usr/bin/env python3
"""Generate derived GitHub-Flavored Markdown from a LaTeX source document."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
MANUAL_FORM_BLOCK_RE = re.compile(
    r"\\begin\{manualformblock\}\{[^{}]*\}|\\end\{manualformblock\}"
)
MANUAL_ABI_CASE_RE = re.compile(r"\\manualabicase\{[^{}]+\}")
LATEX_PART_RE = re.compile(r"\\part(?:\s*\[[^\]]*\])?\s*\{")
ATX_HEADING_RE = re.compile(r"^(#{3,6})([ \t]+)")
FENCE_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})(.*)$")


def normalize_part_heading_levels(markdown: str, *, has_parts: bool) -> str:
    """Collapse Pandoc's unused chapter level below LaTeX part headings."""
    if not has_parts:
        return markdown

    lines: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in markdown.splitlines(keepends=True):
        fence_match = FENCE_RE.match(line.rstrip("\r\n"))
        if fence_match:
            marker = fence_match.group(1)
            suffix = fence_match.group(2)
            if fence_character is None:
                fence_character = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_character and len(marker) >= fence_length and not suffix.strip():
                fence_character = None
                fence_length = 0
            lines.append(line)
            continue

        if fence_character is None:
            line = ATX_HEADING_RE.sub(lambda match: match.group(1)[1:] + match.group(2), line)
        lines.append(line)
    return "".join(lines)


def _run(command: list[str], *, environment: dict[str, str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        cwd=ROOT,
        env=environment,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit status {result.returncode}"
        raise RuntimeError(f"{Path(command[0]).name} failed: {detail}")
    return result


def render_markdown_file(
    source: Path,
    output: Path,
    *,
    pandoc: str = "pandoc",
    latexpand: str = "latexpand",
    environment: dict[str, str] | None = None,
) -> str:
    environment = dict(os.environ if environment is None else environment)
    output.parent.mkdir(parents=True, exist_ok=True)
    expanded_path = output.with_suffix(".expanded.tex")
    _run(
        [
            latexpand,
            "--fatal",
            "--empty-comments",
            "--output",
            str(expanded_path),
            str(source),
        ],
        environment=environment,
    )
    expanded = expanded_path.read_text(encoding="utf-8")
    if re.search(r"\\(?:input|include)\{", expanded):
        raise RuntimeError(f"{source}: latexpand left unresolved input directives")
    unresolved = sorted(set(re.findall(r"@[A-Z0-9_]+@", expanded)))
    if unresolved:
        raise RuntimeError(f"{source}: unresolved template placeholders: {', '.join(unresolved)}")
    expanded = MANUAL_FORM_BLOCK_RE.sub("", expanded)
    expanded = MANUAL_ABI_CASE_RE.sub("", expanded)
    result = subprocess.run(
        [
            pandoc,
            "--from=latex",
            "--to=gfm",
            "--wrap=none",
            "--markdown-headings=atx",
            "--fail-if-warnings",
            f"--resource-path={ROOT}",
        ],
        input=expanded,
        text=True,
        capture_output=True,
        cwd=ROOT,
        env=environment,
        check=False,
    )
    if result.returncode != 0 or result.stderr.strip():
        detail = result.stderr.strip() or f"exit status {result.returncode}"
        raise RuntimeError(f"Pandoc failed to generate Markdown: {detail}")
    markdown = result.stdout.rstrip() + "\n"
    markdown = normalize_part_heading_levels(markdown, has_parts=bool(LATEX_PART_RE.search(expanded)))
    output.write_text(markdown, encoding="utf-8")
    expanded_path.unlink()
    return markdown


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="LaTeX source document")
    parser.add_argument("output", type=Path, help="Derived Markdown output")
    parser.add_argument("--pandoc", help="Pandoc executable")
    args = parser.parse_args()

    render_markdown_file(
        args.input.resolve(),
        args.output.resolve(),
        pandoc=args.pandoc or os.environ.get("PANDOC", "pandoc"),
        latexpand=os.environ.get("LATEXPAND", "latexpand"),
    )
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
