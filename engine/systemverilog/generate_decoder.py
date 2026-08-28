#!/usr/bin/env python3
"""Generate the Bedrock combinational decoder from the current ISA model."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
if __package__ in {None, ""}:
    sys.path.insert(0, str(ROOT))
    from engine.systemverilog import renderer
else:
    from . import renderer


OUTPUT_NAMES = renderer.OUTPUT_NAMES
render_outputs = renderer.render_outputs
write_outputs = renderer.write_outputs
check_outputs = renderer.check_outputs


def main(argv: list[str] | None = None) -> int:
    return int(renderer.main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
