"""Filesystem output for generated artifacts."""

from __future__ import annotations

from pathlib import Path

from .artifact import GeneratedArtifactSet


class ArtifactWriter:
    def write(
        self, artifacts: GeneratedArtifactSet, output_root: str | Path
    ) -> tuple[Path, ...]:
        root = Path(output_root).resolve()
        written: list[Path] = []
        for artifact in artifacts.artifacts:
            destination = (root / artifact.relative_path).resolve()
            if not destination.is_relative_to(root):
                raise ValueError(f"generated artifact escapes output root: {destination}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(artifact.content, encoding="utf-8")
            written.append(destination)
        return tuple(written)
