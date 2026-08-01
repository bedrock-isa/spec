"""Resolve generated document sources from a build-only overlay."""

from __future__ import annotations

import os
from pathlib import Path


OVERLAY_ENV = "BEDROCK_DOCUMENT_OVERLAY"


def overlay_root() -> Path | None:
    value = os.environ.get(OVERLAY_ENV)
    return Path(value).resolve() if value else None


def logical_path(path: Path, repository_root: Path) -> Path:
    resolved = path.resolve()
    try:
        return resolved.relative_to(repository_root.resolve())
    except ValueError as exc:
        raise ValueError(f"{path}: document source is outside {repository_root}") from exc


def resolve_source(path: Path, repository_root: Path) -> Path:
    overlay = overlay_root()
    if overlay is not None:
        candidate = overlay / logical_path(path, repository_root)
        if candidate.is_file():
            return candidate
    return path


def read_source(path: Path, repository_root: Path) -> str:
    return resolve_source(path, repository_root).read_text(encoding="utf-8")


def source_is_file(path: Path, repository_root: Path) -> bool:
    return resolve_source(path, repository_root).is_file()
