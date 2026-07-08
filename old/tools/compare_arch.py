#!/usr/bin/env python3
"""Compare Bedrock code density against external compiler targets.

Bedrock is generated through the local QBE Bedrock backend and bedrock-as.
Reference architectures are generated with external cross compilers so the qbe
tree can stay Bedrock-only.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import struct
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CLANG_TARGETS: dict[str, dict[str, list[str] | str]] = {
    "x86_64": {"triple": "x86_64-unknown-linux-gnu", "extra": []},
    "aarch64": {"triple": "aarch64-unknown-linux-gnu", "extra": []},
    "rv64gc": {"triple": "riscv64-unknown-elf", "extra": ["-march=rv64gc", "-mabi=lp64d"]},
}

GCC_TARGETS: dict[str, dict[str, list[str] | str]] = {
    "m68k": {"compiler_arg": "m68k_gcc", "compiler_default": "m68k-elf-gcc", "extra": ["-m68030"]},
}

DEFAULT_TARGETS = ("bedrock", "m68k", "x86_64", "aarch64", "rv64gc")
TARGET_C_ABI: dict[str, str] = {
    "bedrock": "Bedrock draft C ABI",
    "m68k": "m68k-elf bare-metal C ABI",
    "x86_64": "System V AMD64 psABI",
    "aarch64": "AAPCS64 ELF ABI",
    "rv64gc": "RISC-V ELF psABI LP64D",
}
TARGET_CODE_MODEL: dict[str, str] = {
    "m68k": "absolute32",
    "x86_64": "small",
    "aarch64": "small",
    "rv64gc": "medlow",
}
TARGET_ISA_OPTIONS: dict[str, str] = {
    "bedrock": "ELF64",
    "m68k": "`-m68030`",
    "x86_64": "default",
    "aarch64": "default",
    "rv64gc": "`-march=rv64gc`, `-mabi=lp64d`",
}
TARGET_PIC_MODEL: dict[str, str] = {
    "bedrock": "none",
    "m68k": "none",
    "x86_64": "none",
    "aarch64": "none",
    "rv64gc": "none",
}


def bedrock_code_model(args: argparse.Namespace) -> str:
    return args.bedrock_cmodel


@dataclass
class Row:
    case: str
    target: str
    compiler: str
    c_abi: str
    code_model: str
    text_bytes: int | None
    object_bytes: int | None
    asm_instructions: int | None
    asm_path: str | None
    obj_path: str | None
    status: str
    note: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "case": self.case,
            "target": self.target,
            "compiler": self.compiler,
            "c_abi": self.c_abi,
            "code_model": self.code_model,
            "text_bytes": self.text_bytes,
            "object_bytes": self.object_bytes,
            "asm_instructions": self.asm_instructions,
            "asm_path": self.asm_path,
            "obj_path": self.obj_path,
            "status": self.status,
            "note": self.note,
        }


def run(cmd: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def require_tool(path: str, label: str) -> None:
    if "/" in path:
        if not Path(path).exists():
            raise SystemExit(f"{label} not found: {path}")
    elif shutil.which(path) is None:
        raise SystemExit(f"{label} not found in PATH: {path}")


def read_c_string(blob: bytes, offset: int) -> str:
    end = blob.find(b"\0", offset)
    if end < 0:
        end = len(blob)
    return blob[offset:end].decode("ascii", errors="replace")


def elf_section_sizes(path: Path) -> dict[str, int]:
    data = path.read_bytes()
    if len(data) < 16 or data[:4] != b"\x7fELF":
        raise ValueError(f"not an ELF object: {path}")
    elf_class = data[4]
    endian = "<" if data[5] == 1 else ">"
    if elf_class == 1:
        header_fmt = endian + "HHIIIIIHHHHHH"
        header = struct.unpack_from(header_fmt, data, 16)
        e_shoff = header[5]
        e_shentsize = header[10]
        e_shnum = header[11]
        e_shstrndx = header[12]
        sh_fmt = endian + "IIIIIIIIII"
        sh_name_i = 0
        sh_offset_i = 4
        sh_size_i = 5
    elif elf_class == 2:
        header_fmt = endian + "HHIQQQIHHHHHH"
        header = struct.unpack_from(header_fmt, data, 16)
        e_shoff = header[5]
        e_shentsize = header[10]
        e_shnum = header[11]
        e_shstrndx = header[12]
        sh_fmt = endian + "IIQQQQIIQQ"
        sh_name_i = 0
        sh_offset_i = 4
        sh_size_i = 5
    else:
        raise ValueError(f"unsupported ELF class {elf_class}: {path}")

    sections = []
    for index in range(e_shnum):
        offset = e_shoff + index * e_shentsize
        sections.append(struct.unpack_from(sh_fmt, data, offset))
    if e_shstrndx >= len(sections):
        return {}
    strtab = sections[e_shstrndx]
    strtab_data = data[int(strtab[sh_offset_i]) : int(strtab[sh_offset_i] + strtab[sh_size_i])]
    sizes: dict[str, int] = {}
    for section in sections:
        name = read_c_string(strtab_data, int(section[sh_name_i]))
        sizes[name] = int(section[sh_size_i])
    return sizes


def count_asm_instructions(path: Path) -> int:
    count = 0
    label_with_comment = re.compile(r"^[A-Za-z_.$][A-Za-z0-9_.$]*:\s*(?://|#|@|/\*|$)")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        text = line.strip()
        if not text:
            continue
        if (
            text.endswith(":")
            or label_with_comment.match(text)
            or text == "}"
            or text.endswith("{")
            or text.startswith((".", "#", "@", "//", "/*", "*"))
        ):
            continue
        count += 1
    return count


def row_from_artifacts(case: str, target: str, compiler: str, asm: Path, obj: Path) -> Row:
    try:
        text_bytes = elf_section_sizes(obj).get(".text", 0)
        note = ""
    except Exception as exc:  # noqa: BLE001 - report object parser failure in row.
        text_bytes = None
        note = str(exc)
    return Row(
        case=case,
        target=target,
        compiler=compiler,
        c_abi=TARGET_C_ABI.get(target, "unknown"),
        code_model=TARGET_CODE_MODEL.get(target, "unknown"),
        text_bytes=text_bytes,
        object_bytes=obj.stat().st_size if obj.exists() else None,
        asm_instructions=count_asm_instructions(asm) if asm.exists() else None,
        asm_path=str(asm),
        obj_path=str(obj),
        status="ok" if text_bytes is not None else "failed",
        note=note,
    )


def build_bedrock(source: Path, case_dir: Path, args: argparse.Namespace) -> Row:
    stem = source.stem
    ssa = case_dir / f"{stem}.bedrock.ssa"
    asm = case_dir / f"{stem}.bedrock.s"
    obj = case_dir / f"{stem}.bedrock.o"
    if source.suffix == ".ssa":
        ssa.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        minic = run([args.minic], input_text=source.read_text(encoding="utf-8"))
        if minic.returncode != 0:
            return Row(stem, "bedrock", "qbe+bedrock-as", TARGET_C_ABI["bedrock"], bedrock_code_model(args), None, None, None, None, None, "failed", minic.stderr.strip())
        ssa.write_text(minic.stdout, encoding="utf-8")

    qbe = run([args.qbe, "-t", "bedrock", "-G", "e", "-m", args.bedrock_cmodel, "-o", str(asm), str(ssa)])
    if qbe.returncode != 0:
        return Row(stem, "bedrock", "qbe+bedrock-as", TARGET_C_ABI["bedrock"], bedrock_code_model(args), None, None, None, str(asm), None, "failed", qbe.stderr.strip())
    assembler = run([args.bedrock_as, "-o", str(obj), str(asm)])
    if assembler.returncode != 0:
        return Row(stem, "bedrock", "qbe+bedrock-as", TARGET_C_ABI["bedrock"], bedrock_code_model(args), None, None, None, str(asm), str(obj), "failed", assembler.stderr.strip())
    row = row_from_artifacts(stem, "bedrock", "qbe+bedrock-as", asm, obj)
    row.code_model = bedrock_code_model(args)
    return row


def clang_flags(args: argparse.Namespace, target: str) -> list[str]:
    meta = CLANG_TARGETS[target]
    return [
        args.clang,
        "-target",
        str(meta["triple"]),
        f"-{args.opt}",
        "-std=gnu89",
        "-Wno-implicit-int",
        "-Wno-return-type",
        "-ffreestanding",
        "-nostdlib",
        "-fno-builtin",
        "-fno-stack-protector",
        "-fno-unwind-tables",
        "-fno-asynchronous-unwind-tables",
        *list(meta["extra"]),
    ]


def gcc_flags(args: argparse.Namespace, target: str) -> list[str]:
    meta = GCC_TARGETS[target]
    compiler = getattr(args, str(meta["compiler_arg"]))
    return [
        compiler,
        f"-{args.opt}",
        "-std=gnu89",
        "-Wno-implicit-int",
        "-Wno-return-type",
        "-ffreestanding",
        "-nostdlib",
        "-fno-builtin",
        "-fno-stack-protector",
        "-fno-unwind-tables",
        "-fno-asynchronous-unwind-tables",
        *list(meta["extra"]),
    ]


def build_clang(source: Path, target: str, case_dir: Path, args: argparse.Namespace) -> Row:
    stem = source.stem
    asm = case_dir / f"{stem}.{target}.s"
    obj = case_dir / f"{stem}.{target}.o"
    flags = clang_flags(args, target)
    emit_asm = run([*flags, "-S", str(source), "-o", str(asm)])
    if emit_asm.returncode != 0:
        return Row(stem, target, str(CLANG_TARGETS[target]["triple"]), TARGET_C_ABI[target], TARGET_CODE_MODEL[target], None, None, None, str(asm), None, "failed", emit_asm.stderr.strip())
    emit_obj = run([*flags, "-c", str(source), "-o", str(obj)])
    if emit_obj.returncode != 0:
        return Row(stem, target, str(CLANG_TARGETS[target]["triple"]), TARGET_C_ABI[target], TARGET_CODE_MODEL[target], None, None, None, str(asm), str(obj), "failed", emit_obj.stderr.strip())
    return row_from_artifacts(stem, target, str(CLANG_TARGETS[target]["triple"]), asm, obj)


def build_gcc(source: Path, target: str, case_dir: Path, args: argparse.Namespace) -> Row:
    stem = source.stem
    asm = case_dir / f"{stem}.{target}.s"
    obj = case_dir / f"{stem}.{target}.o"
    flags = gcc_flags(args, target)
    compiler = Path(flags[0]).name
    label = f"{compiler} {' '.join(str(item) for item in GCC_TARGETS[target]['extra'])}".strip()
    emit_asm = run([*flags, "-S", str(source), "-o", str(asm)])
    if emit_asm.returncode != 0:
        return Row(stem, target, label, TARGET_C_ABI[target], TARGET_CODE_MODEL[target], None, None, None, str(asm), None, "failed", emit_asm.stderr.strip())
    emit_obj = run([*flags, "-c", str(source), "-o", str(obj)])
    if emit_obj.returncode != 0:
        return Row(stem, target, label, TARGET_C_ABI[target], TARGET_CODE_MODEL[target], None, None, None, str(asm), str(obj), "failed", emit_obj.stderr.strip())
    return row_from_artifacts(stem, target, label, asm, obj)


def discover_cases(paths: list[str]) -> list[Path]:
    cases: list[Path] = []
    for item in paths:
        path = Path(item)
        if path.is_dir():
            cases.extend(sorted(path.glob("*.c")))
            cases.extend(sorted(path.glob("*.ssa")))
        else:
            cases.append(path)
    return cases


def render_report(rows: list[Row], args: argparse.Namespace) -> str:
    by_case: dict[str, dict[str, Row]] = {}
    bedrock_bytes: dict[str, int] = {}
    for row in rows:
        by_case.setdefault(row.case, {})[row.target] = row
        if row.target == "bedrock" and row.text_bytes:
            bedrock_bytes[row.case] = row.text_bytes

    cases = sorted(by_case)
    targets = list(args.targets)

    def row_for(case: str, target: str) -> Row | None:
        return by_case.get(case, {}).get(target)

    def text_cell(case: str, target: str) -> str:
        row = row_for(case, target)
        if row is None:
            return "-"
        if row.text_bytes is None:
            return row.status
        return str(row.text_bytes)

    def ratio_cell(case: str, target: str) -> str:
        row = row_for(case, target)
        base = bedrock_bytes.get(case)
        if row is None or row.text_bytes is None or not base:
            return "-"
        if target == "bedrock":
            return "1.00x"
        return f"{row.text_bytes / base:.2f}x"

    def instr_cell(case: str, target: str) -> str:
        row = row_for(case, target)
        if row is None:
            return "-"
        if row.asm_instructions is None:
            return row.status
        return str(row.asm_instructions)

    def object_cell(case: str, target: str) -> str:
        row = row_for(case, target)
        if row is None:
            return "-"
        if row.object_bytes is None:
            return row.status
        return str(row.object_bytes)

    def target_header() -> str:
        return " | ".join(f"`{target}`" for target in targets)

    def target_align() -> str:
        return " | ".join("---:" for _ in targets)

    def case_table(case: str) -> list[str]:
        out = [
            f"## `{case}`",
            "",
            f"| Case | {target_header()} |",
            f"| --- | {target_align()} |",
            f"| ASM instruction count | {' | '.join(instr_cell(case, target) for target in targets)} |",
            f"| .text bytes | {' | '.join(text_cell(case, target) for target in targets)} |",
            f"| vs Bedrock | {' | '.join(ratio_cell(case, target) for target in targets)} |",
            f"| Object bytes | {' | '.join(object_cell(case, target) for target in targets)} |",
        ]
        out.append("")
        return out

    def target_context_table() -> list[str]:
        out = [
            "## Target ABI Context",
            "",
            "| Target | Toolchain | ISA/options | Code model | PIC/PIE | C ABI |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for target in targets:
            row = next((item for item in rows if item.target == target), None)
            compiler = row.compiler if row is not None else "-"
            code_model = row.code_model if row is not None else TARGET_CODE_MODEL.get(target, "unknown")
            c_abi = row.c_abi if row is not None else TARGET_C_ABI.get(target, "unknown")
            isa_options = TARGET_ISA_OPTIONS.get(target, "unknown")
            pic_model = TARGET_PIC_MODEL.get(target, "unknown")
            out.append(f"| `{target}` | `{compiler}` | {isa_options} | `{code_model}` | `{pic_model}` | {c_abi} |")
        out.append("")
        return out

    failures = [
        row for row in rows
        if row.status != "ok" and not (row.status == "skipped" and row.note)
    ]
    skipped = [row for row in rows if row.status == "skipped"]

    lines = [
        "# Architecture Code-Density Comparison",
        "",
        f"- Optimization: `-{args.opt}` for reference targets",
        f"- Bedrock code model: `{args.bedrock_cmodel}`",
        f"- Targets: {', '.join(targets)}",
        f"- Output directory: `{args.out_dir}`",
        "",
    ]
    lines.extend(target_context_table())
    for case in cases:
        lines.extend(case_table(case))
    if failures or skipped:
        lines.extend(["## Notes", ""])
        for row in failures + skipped:
            note = row.note.splitlines()[0] if row.note else row.status
            lines.append(f"- `{row.case}` / `{row.target}`: {row.status}: {note}")
        lines.append("")
    lines.append("")
    lines.append("Artifacts are emitted per case under the output directory.")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", nargs="*", default=["benchmarks/arch_compare"])
    parser.add_argument("--targets", nargs="+", default=list(DEFAULT_TARGETS), choices=["bedrock", *GCC_TARGETS.keys(), *CLANG_TARGETS.keys()])
    parser.add_argument("--out-dir", default="build/compare/arch")
    parser.add_argument("--report", default="build/compare/arch_compare.md")
    parser.add_argument("--json", default="build/compare/arch_compare.json")
    parser.add_argument("--qbe", default="build/qbe/obj/qbe")
    parser.add_argument("--minic", default="qbe/minic/minic")
    parser.add_argument("--bedrock-as", default="build/host/bedrock-as")
    parser.add_argument("--bedrock-cmodel", default="small", choices=["small", "low", "high", "large"])
    parser.add_argument("--clang", default="clang")
    parser.add_argument("--m68k-gcc", default=str(GCC_TARGETS["m68k"]["compiler_default"]))
    parser.add_argument("--opt", default="Oz", choices=["O0", "O1", "O2", "O3", "Os", "Oz"])
    args = parser.parse_args(argv)

    if "bedrock" in args.targets:
        require_tool(args.qbe, "qbe")
        require_tool(args.minic, "minic")
        require_tool(args.bedrock_as, "bedrock-as")
    if any(target in CLANG_TARGETS for target in args.targets):
        require_tool(args.clang, "clang")
    for target in args.targets:
        if target in GCC_TARGETS:
            require_tool(getattr(args, str(GCC_TARGETS[target]["compiler_arg"])), target)

    out_dir = Path(args.out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cases = discover_cases(args.cases)
    rows: list[Row] = []
    for source in cases:
        case_dir = out_dir / source.stem
        case_dir.mkdir(parents=True, exist_ok=True)
        for target in args.targets:
            if source.suffix == ".ssa" and target != "bedrock":
                rows.append(Row(source.stem, target, "n/a", TARGET_C_ABI.get(target, "unknown"), TARGET_CODE_MODEL.get(target, "unknown"), None, None, None, None, None, "skipped", "SSA input is Bedrock-only"))
            elif target == "bedrock":
                rows.append(build_bedrock(source, case_dir, args))
            elif target in GCC_TARGETS:
                rows.append(build_gcc(source, target, case_dir, args))
            else:
                rows.append(build_clang(source, target, case_dir, args))

    report = render_report(rows, args)
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text(report, encoding="utf-8")
    Path(args.json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json).write_text(json.dumps([row.as_dict() for row in rows], indent=2) + "\n", encoding="utf-8")
    sys.stdout.write(report)
    return 1 if any(row.status == "failed" for row in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
