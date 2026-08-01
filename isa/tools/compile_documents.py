#!/usr/bin/env python3
"""Compile and validate the complete Bedrock document set."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = Path(__file__).resolve().parent
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from artifact_overlay import OVERLAY_ENV  # noqa: E402
import gen_abi_tables  # noqa: E402
import gen_architecture_tables  # noqa: E402
import gen_docs  # noqa: E402
import gen_target_intrinsics  # noqa: E402
from latex_to_markdown import render_markdown_file  # noqa: E402


GENERATED_INCLUDE_RE = re.compile(r"\\(?:input|include)\{([^{}]+)\}")
LOG_FAILURE_PATTERNS = (
    re.compile(r"LaTeX Warning: There were undefined references"),
    re.compile(r"LaTeX Warning: Reference .* undefined"),
    re.compile(r"LaTeX Warning: Citation .* undefined"),
    re.compile(r"LaTeX Warning: Label\(s\) may have changed"),
    re.compile(r"Rerun to get cross-references right"),
    re.compile(r"Package rerunfilecheck Warning: File .* has changed"),
    re.compile(r"Missing character:"),
    re.compile(r"Overfull \\[hv]box"),
    re.compile(r"destination with the same identifier"),
)
UNDERFULL_RE = re.compile(r"Underfull \\([hv])box")


@dataclass(frozen=True)
class Document:
    key: str
    source: Path | None
    pdf_name: str
    pdf_output: Path
    markdown_output: Path


DOCUMENTS = (
    Document(
        "isa-reference",
        None,
        "isa_reference.pdf",
        Path("isa_reference.pdf"),
        Path("isa_reference.md"),
    ),
    Document(
        "bedrock-elf-abi",
        ROOT / "isa" / "abi" / "bedrock-elf-abi.tex",
        "bedrock-elf-abi.pdf",
        Path("latex/bedrock-elf-abi/bedrock-elf-abi.pdf"),
        Path("markdown/bedrock-elf-abi.md"),
    ),
    Document(
        "bedrock-c-abi",
        ROOT / "isa" / "abi" / "bedrock-c-abi.tex",
        "bedrock-c-abi.pdf",
        Path("latex/bedrock-c-abi/bedrock-c-abi.pdf"),
        Path("markdown/bedrock-c-abi.md"),
    ),
    Document(
        "bedrock-c-far-extensions",
        ROOT / "isa" / "c" / "bedrock-c-far-extensions.tex",
        "bedrock-c-far-extensions.pdf",
        Path("latex/bedrock-c-far-extensions/bedrock-c-far-extensions.pdf"),
        Path("markdown/bedrock-c-far-extensions.md"),
    ),
    Document(
        "bedrock-target-intrinsics",
        ROOT / "isa" / "c" / "bedrock-target-intrinsics.tex",
        "bedrock-target-intrinsics.pdf",
        Path("latex/bedrock-target-intrinsics/bedrock-target-intrinsics.pdf"),
        Path("markdown/bedrock-target-intrinsics.md"),
    ),
    Document(
        "bedrock-programming-toolchain-guide",
        ROOT / "isa" / "guides" / "bedrock-programming-toolchain-guide.tex",
        "bedrock-programming-toolchain-guide.pdf",
        Path("latex/bedrock-programming-toolchain-guide/bedrock-programming-toolchain-guide.pdf"),
        Path("markdown/bedrock-programming-toolchain-guide.md"),
    ),
)


class CompileError(RuntimeError):
    """The document set cannot be compiled safely."""


class ArtifactStore:
    def __init__(self) -> None:
        self._contents: dict[Path, str] = {}
        self._sources: dict[Path, str] = {}
        self._consumed: set[Path] = set()

    @staticmethod
    def _logical(path: Path) -> Path:
        resolved = path.resolve()
        try:
            logical = resolved.relative_to(ROOT)
        except ValueError as exc:
            raise CompileError(f"generated artifact is outside the repository: {path}") from exc
        if logical.is_absolute() or ".." in logical.parts:
            raise CompileError(f"invalid generated artifact path: {path}")
        return logical

    def add_all(self, outputs: dict[Path, str], producer: str) -> None:
        for path, content in outputs.items():
            logical = self._logical(path)
            previous = self._sources.get(logical)
            if previous is not None:
                raise CompileError(
                    f"generated artifact {logical} is produced by both {previous} and {producer}"
                )
            self._contents[logical] = content
            self._sources[logical] = producer

    def materialize(self, overlay: Path) -> None:
        for logical, content in self._contents.items():
            destination = overlay / logical
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")

    def mark_consumed(self, logical: Path) -> None:
        normalized = Path(str(logical).removesuffix(".tex"))
        candidates = (logical, normalized.with_suffix(".tex"))
        for candidate in candidates:
            if candidate in self._contents:
                self._consumed.add(candidate)

    def discover_consumers(self, texts: Iterable[str]) -> None:
        for text in texts:
            for match in GENERATED_INCLUDE_RE.finditer(text):
                self.mark_consumed(Path(match.group(1)))

    def require_all_consumed(self) -> None:
        unused = sorted(set(self._contents) - self._consumed)
        if unused:
            details = ", ".join(f"{path} ({self._sources[path]})" for path in unused)
            raise CompileError(f"generated artifacts have no document consumer: {details}")

    def require_absent_from_source_tree(self) -> None:
        leaked = sorted(logical for logical in self._contents if (ROOT / logical).exists())
        if leaked:
            raise CompileError(
                "generated TeX must exist only in the build overlay: "
                + ", ".join(str(path) for path in leaked)
            )

    @property
    def count(self) -> int:
        return len(self._contents)


def run(
    command: list[str],
    *,
    env: dict[str, str],
    cwd: Path = ROOT,
    description: str,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = "\n".join(part for part in (result.stdout.strip(), result.stderr.strip()) if part)
        raise CompileError(f"{description} failed:\n{detail}")
    return result


def source_snapshot(output_root: Path) -> dict[str, str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    try:
        excluded_output = output_root.resolve().relative_to(ROOT)
    except ValueError:
        excluded_output = None
    snapshot: dict[str, str] = {}
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        relative = raw.decode("utf-8")
        logical = Path(relative)
        if excluded_output is not None and (
            logical == excluded_output or excluded_output in logical.parents
        ):
            continue
        path = ROOT / relative
        if path.is_file():
            snapshot[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            snapshot[relative] = "<missing>"
    return snapshot


def validation_commands() -> tuple[tuple[str, list[str]], ...]:
    python = sys.executable
    return (
        ("schema validation", [python, "isa/tools/validate_schema.py"]),
        ("definition validation", [python, "isa/tools/validate_defs.py"]),
        ("allocation validation", [python, "isa/tools/validate_alloc.py"]),
        ("ISA join validation", [python, "isa/tools/validate_isa.py"]),
        ("ABI and compiler-interface validation", [python, "isa/tools/validate_abi_docs.py"]),
        ("conformance validation", [python, "isa/tools/validate_conformance.py"]),
        ("reference navigation validation", [python, "isa/tools/validate_reference_navigation.py"]),
    )


def source_texts(isa_latex: str) -> list[str]:
    texts = [isa_latex]
    for root in (ROOT / "isa",):
        for path in root.rglob("*"):
            if path.suffix in {".tex", ".in"} and path.is_file():
                texts.append(path.read_text(encoding="utf-8"))
    return texts


def latex_environment(base: dict[str, str], overlay: Path) -> dict[str, str]:
    env = dict(base)
    roots = (str(overlay), str(ROOT), "")
    env["TEXINPUTS"] = os.pathsep.join(roots)
    env[OVERLAY_ENV] = str(overlay)
    return env


def inspect_latex_log(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="replace")
    failures = [pattern.pattern for pattern in LOG_FAILURE_PATTERNS if pattern.search(text)]
    if failures:
        raise CompileError(f"{path}: forbidden LaTeX diagnostics: {', '.join(failures)}")
    locations: list[dict[str, object]] = []
    for match in UNDERFULL_RE.finditer(text):
        line_start = text.rfind("\n", 0, match.start()) + 1
        line_end = text.find("\n", match.end())
        if line_end < 0:
            line_end = len(text)
        diagnostic = text[line_start:line_end].strip()
        tex_line_match = re.search(r"\bat lines? ([0-9]+(?:--[0-9]+)?)", diagnostic)
        locations.append(
            {
                "kind": f"{match.group(1)}box",
                "log_line": text.count("\n", 0, match.start()) + 1,
                "tex_lines": tex_line_match.group(1) if tex_line_match else None,
            }
        )
    return {
        "underfull_boxes": len(locations),
        "underfull_locations": locations,
    }


def inspect_pdf(path: Path, env: dict[str, str]) -> dict[str, int]:
    info = run(["pdfinfo", str(path)], env=env, description=f"pdfinfo for {path}")
    match = re.search(r"^Pages:\s+(\d+)$", info.stdout, flags=re.MULTILINE)
    if not match or int(match.group(1)) <= 0:
        raise CompileError(f"{path}: PDF has no readable pages")
    fonts = run(["pdffonts", str(path)], env=env, description=f"pdffonts for {path}")
    rows = fonts.stdout.splitlines()[2:]
    if not rows:
        raise CompileError(f"{path}: PDF contains no fonts")
    for row in rows:
        columns = row.split()
        if len(columns) < 6 or columns[-5] != "yes":
            raise CompileError(f"{path}: unembedded or unreadable font row: {row}")
    return {"pages": int(match.group(1)), "fonts": len(rows)}


def compile_pdf(
    document: Document,
    source: Path,
    stage: Path,
    env: dict[str, str],
    latexmk: str,
) -> tuple[Path, Path, dict[str, object]]:
    output_dir = stage / "latex" / document.key
    output_dir.mkdir(parents=True, exist_ok=True)
    run(
        [
            latexmk,
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            f"-outdir={output_dir}",
            str(source),
        ],
        env=env,
        description=f"LaTeX compilation for {document.key}",
    )
    pdf = output_dir / document.pdf_name
    log = output_dir / (Path(document.pdf_name).stem + ".log")
    if not pdf.is_file() or not log.is_file():
        raise CompileError(f"{document.key}: expected PDF or log was not produced")
    metrics = inspect_latex_log(log)
    metrics.update(inspect_pdf(pdf, env))
    return pdf, log, metrics


def publish_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")
    shutil.copy2(source, temporary)
    os.replace(temporary, destination)


def compile_documents(args: argparse.Namespace) -> int:
    output_root = args.output_root.resolve()
    if output_root in {Path("/").resolve(), Path.home().resolve(), ROOT.resolve()}:
        raise CompileError(f"refusing unsafe output root: {output_root}")
    before = source_snapshot(output_root)
    stage = output_root / f".doc-compile-{os.getpid()}"
    if stage.exists():
        shutil.rmtree(stage)
    overlay = stage / "overlay"
    overlay.mkdir(parents=True)
    env = latex_environment(os.environ, overlay)

    store = ArtifactStore()
    store.add_all(gen_architecture_tables.render_artifacts(), "architecture tables")
    store.add_all(gen_abi_tables.render_artifacts(), "ABI tables")
    store.add_all(gen_target_intrinsics.render_artifacts(), "target intrinsic tables")
    store.require_absent_from_source_tree()
    store.materialize(overlay)

    for description, command in validation_commands():
        run(command, env=env, description=description)

    model = gen_docs.load_model(gen_docs.DEF_ROOT)
    store.add_all(
        gen_docs.render_ea_reference_fragments(model.metadata.get("ea") or {}),
        "effective-address reference",
    )
    store.require_absent_from_source_tree()
    store.materialize(overlay)
    isa_latex = gen_docs.render_latex(model)
    isa_source = stage / "isa_reference.tex"
    isa_source.write_text(isa_latex, encoding="utf-8")

    store.discover_consumers(source_texts(isa_latex))
    store.mark_consumed(Path("isa/defs/instructions/RDPMC/details.tex"))
    store.require_all_consumed()

    sources = {
        document.key: isa_source if document.source is None else document.source
        for document in DOCUMENTS
    }
    metrics: dict[str, dict[str, object]] = {}
    produced_pdfs: dict[str, tuple[Path, Path]] = {}
    produced_markdown: dict[str, Path] = {}

    if args.format in {"all", "pdf"}:
        for document in DOCUMENTS:
            pdf, log, document_metrics = compile_pdf(
                document, sources[document.key], stage, env, args.latexmk
            )
            produced_pdfs[document.key] = (pdf, log)
            metrics[document.key] = document_metrics

    if args.format in {"all", "markdown"}:
        for document in DOCUMENTS:
            markdown = stage / "markdown" / document.markdown_output.name
            markdown.parent.mkdir(parents=True, exist_ok=True)
            render_markdown_file(
                sources[document.key],
                markdown,
                pandoc=args.pandoc,
                latexpand=args.latexpand,
                environment=env,
            )
            produced_markdown[document.key] = markdown

    after = source_snapshot(output_root)
    store.require_absent_from_source_tree()
    if before != after:
        changed = sorted(key for key in set(before) | set(after) if before.get(key) != after.get(key))
        raise CompileError("document compilation modified tracked sources: " + ", ".join(changed))

    for document in DOCUMENTS:
        if document.key in produced_pdfs:
            pdf, log = produced_pdfs[document.key]
            publish_file(pdf, output_root / document.pdf_output)
            publish_file(log, (output_root / document.pdf_output).with_suffix(".log"))
        if document.key in produced_markdown:
            publish_file(produced_markdown[document.key], output_root / document.markdown_output)
    if args.format in {"all", "pdf"}:
        publish_file(isa_source, output_root / "isa_reference.tex")

    generated_destination = output_root / "generated"
    if generated_destination.exists():
        shutil.rmtree(generated_destination)
    shutil.copytree(overlay, generated_destination)

    report = {
        "format": args.format,
        "generated_artifacts": store.count,
        "documents": metrics,
    }
    report_path = stage / "document-compile.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    publish_file(report_path, output_root / "document-compile.json")
    shutil.rmtree(stage)
    print(
        f"compiled {len(DOCUMENTS)} documents; "
        f"{store.count} generated TeX artifacts; report: {output_root / 'document-compile.json'}"
    )
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("all", "pdf", "markdown"), default="all")
    parser.add_argument("--output-root", type=Path, default=ROOT / "build")
    parser.add_argument("--latexmk", default=os.environ.get("LATEXMK", "latexmk"))
    parser.add_argument("--pandoc", default=os.environ.get("PANDOC", "pandoc"))
    parser.add_argument("--latexpand", default=os.environ.get("LATEXPAND", "latexpand"))
    return parser.parse_args()


def main() -> int:
    try:
        return compile_documents(parse_args())
    except (CompileError, OSError, RuntimeError, ValueError) as exc:
        print(f"document compilation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
