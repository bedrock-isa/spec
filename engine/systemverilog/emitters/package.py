"""Emit the public decoder package around lowered declarations."""

from __future__ import annotations

from ..templates import render_template


def render(*, declarations: str) -> str:
    return render_template(
        "bedrock_decode_pkg.sv.in", {"PACKAGE_DECLARATIONS": declarations}
    )
