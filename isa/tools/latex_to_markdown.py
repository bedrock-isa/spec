#!/usr/bin/env python3
"""Generate derived GitHub-Flavored Markdown from a LaTeX source document."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[2]
LATEX_INPUT_RE = re.compile(r"\\(?:input|include)\{([^{}]+)\}")
MANUAL_FORM_BLOCK_RE = re.compile(
    r"\\begin\{manualformblock\}\{[^{}]*\}|\\end\{manualformblock\}"
)


def resolve_latex_input(name: str, current_dir: Path) -> Path:
    relative = Path(name)
    candidates = [current_dir / relative, ROOT / relative]
    if not relative.suffix:
        candidates.extend([current_dir / f"{name}.tex", ROOT / f"{name}.tex"])
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise FileNotFoundError(f"LaTeX input not found: {name}")


def expand_latex_inputs(
    text: str,
    *,
    current_dir: Path = ROOT,
    stack: tuple[Path, ...] = (),
) -> str:
    def replace(match: re.Match[str]) -> str:
        path = resolve_latex_input(match.group(1), current_dir)
        if path in stack:
            chain = " -> ".join(str(item) for item in (*stack, path))
            raise ValueError(f"recursive LaTeX input: {chain}")
        source = path.read_text(encoding="utf-8")
        return expand_latex_inputs(source, current_dir=path.parent, stack=(*stack, path))

    return LATEX_INPUT_RE.sub(replace, text)


def render_markdown_from_latex(
    text: str,
    pandoc: str | None = None,
    *,
    current_dir: Path = ROOT,
) -> str:
    executable = pandoc or os.environ.get("PANDOC") or shutil.which("pandoc")
    if not executable:
        raise RuntimeError(
            "Pandoc is required for Markdown output. Install pandoc or set PANDOC to its executable path."
        )
    expanded = expand_latex_inputs(text, current_dir=current_dir)
    expanded = MANUAL_FORM_BLOCK_RE.sub("", expanded)
    try:
        result = subprocess.run(
            [
                executable,
                "--from=latex",
                "--to=gfm",
                "--wrap=none",
                "--markdown-headings=atx",
                f"--resource-path={ROOT}",
            ],
            input=expanded,
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
    except OSError as exc:
        raise RuntimeError(f"Cannot execute Pandoc at {executable}: {exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.strip() or f"exit status {result.returncode}"
        raise RuntimeError(f"Pandoc failed to generate Markdown: {detail}")
    return result.stdout.rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="LaTeX source document")
    parser.add_argument("output", type=Path, help="Derived Markdown output")
    parser.add_argument("--pandoc", help="Pandoc executable")
    args = parser.parse_args()

    source_path = args.input.resolve()
    source = source_path.read_text(encoding="utf-8")
    markdown = render_markdown_from_latex(
        source,
        args.pandoc,
        current_dir=source_path.parent,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
