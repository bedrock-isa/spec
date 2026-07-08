"""Small template helpers for generated tool artifacts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping


TEMPLATE_DIR = Path(__file__).parent / "templates"
PLACEHOLDER_RE = re.compile(r"@[A-Z0-9_]+@")


def load_tool_template(name: str) -> str:
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8")


def render_tool_template(name: str, values: Mapping[str, Any]) -> str:
    text = load_tool_template(name)
    for key, value in values.items():
        text = text.replace(f"@{key}@", str(value))
    missing = sorted(set(PLACEHOLDER_RE.findall(text)))
    if missing:
        raise ValueError(f"{name}: unresolved template placeholders: {', '.join(missing)}")
    return text
