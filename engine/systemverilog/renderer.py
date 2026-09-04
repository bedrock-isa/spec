"""Assemble lowered decoder sections into artifact-owned RTL outputs."""

from __future__ import annotations

from pathlib import Path

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


def render_outputs() -> dict[Path, str]:
    """Return relative outputs for consumption by declared artifact owners."""

    ir = decode_ir.load_decode_ir(ROOT / "isa" / "instructions" / "definitions")
    outputs = lowering.lower(ir)
    return {
        Path(OUTPUT_NAMES[0]): outputs.package,
        Path(OUTPUT_NAMES[1]): outputs.d0,
        Path(OUTPUT_NAMES[2]): outputs.d1,
        Path(OUTPUT_NAMES[3]): outputs.ea,
    }
