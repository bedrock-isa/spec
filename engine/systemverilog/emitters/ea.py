"""Emit the EA decoder from lowered parsing functions."""

from __future__ import annotations

from ..templates import render_template


def render(*, parsing_functions: str) -> str:
    return render_template(
        "bedrock_decode_ea.sv.in", {"EA_PARSING_FUNCTIONS": parsing_functions}
    )
