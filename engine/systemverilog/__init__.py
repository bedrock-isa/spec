"""SystemVerilog decoder generation from the canonical ISA model."""

from .renderer import OUTPUT_NAMES, render_outputs

__all__ = [
    "OUTPUT_NAMES",
    "render_outputs",
]
