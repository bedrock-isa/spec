"""Emit the D0 decoder from lowered sections."""

from __future__ import annotations

from typing import Mapping

from ..templates import render_template


def render(sections: Mapping[str, object]) -> str:
    return render_template("bedrock_decode_d0.sv.in", sections)
