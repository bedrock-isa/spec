#!/usr/bin/env python3
"""Assemble lowered decoder sections into RTL outputs."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import tempfile

from . import decoder_ir as decode_ir
from . import lowering


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_NAMES = (
    "bedrock_decode_pkg.sv",
    "bedrock_decode_d0.sv",
    "bedrock_decode_d1.sv",
    "bedrock_decode_ea.sv",
)

Names = lowering.Names
PublicLayout = lowering.PublicLayout
derive_public_layout = lowering.derive_public_layout
representative_opcode = lowering.representative_opcode
reference_d0 = lowering.reference_d0
reference_d1 = lowering.reference_d1
reference_ea = lowering.reference_ea


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def validate_build_dir(raw_build_dir: Path) -> Path:
    """Accept only a repository build subtree or a dedicated external temp path."""
    build_dir = raw_build_dir.expanduser().resolve()
    repository_build = (ROOT / "build").resolve()
    if _is_within(build_dir, repository_build):
        return build_dir
    temp_roots = {
        Path(tempfile.gettempdir()).resolve(),
        Path("/private/tmp").resolve(),
        Path("/tmp").resolve(),
        Path("/var/tmp").resolve(),
    }
    if not _is_within(build_dir, ROOT) and any(
        build_dir != root and _is_within(build_dir, root) for root in temp_roots
    ):
        return build_dir
    raise ValueError(
        f"refusing SystemVerilog build directory outside {repository_build} "
        f"or an external temporary directory: {build_dir}"
    )


def render_outputs(build_dir: Path) -> dict[Path, str]:
    ir = decode_ir.load_decode_ir(ROOT / "isa" / "instructions" / "definitions")
    outputs = lowering.lower(ir)
    return {
        build_dir / OUTPUT_NAMES[0]: outputs.package,
        build_dir / OUTPUT_NAMES[1]: outputs.d0,
        build_dir / OUTPUT_NAMES[2]: outputs.d1,
        build_dir / OUTPUT_NAMES[3]: outputs.ea,
    }


def write_outputs(build_dir: Path) -> None:
    build_dir = validate_build_dir(build_dir)
    for path, text in render_outputs(build_dir).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def check_outputs(build_dir: Path) -> bool:
    build_dir = validate_build_dir(build_dir)
    return all(
        path.exists() and path.read_text(encoding="utf-8") == expected
        for path, expected in render_outputs(build_dir).items()
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "build_dir",
        metavar="BUILD_DIR",
        type=Path,
        help="directory beneath repository build/ or a dedicated external temp directory",
    )
    parser.add_argument(
        "--check", action="store_true", help="fail if generated output is stale"
    )
    args = parser.parse_args(argv)
    try:
        build_dir = validate_build_dir(args.build_dir)
        outputs = render_outputs(build_dir)
    except (OSError, ValueError) as error:
        print(f"SystemVerilog decoder generation failed: {error}", file=sys.stderr)
        return 1
    if args.check:
        stale = [
            path
            for path, expected in outputs.items()
            if not path.exists() or path.read_text(encoding="utf-8") != expected
        ]
        for path in stale:
            print(f"stale generated output: {path}", file=sys.stderr)
        return int(bool(stale))
    write_outputs(build_dir)
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
