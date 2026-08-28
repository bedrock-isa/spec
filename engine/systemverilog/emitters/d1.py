"""Emit the D1 decoder from lowered sections."""

from __future__ import annotations

from ..templates import render_template


def render(
    *,
    ea_span_function: str,
    form_cases: str,
) -> str:
    return render_template(
        "bedrock_decode_d1.sv.in",
        {
            "EA_SPAN_FUNCTION": ea_span_function,
            "FORM_CASES": form_cases,
        },
    )
