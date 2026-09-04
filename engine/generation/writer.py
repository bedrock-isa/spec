"""Filesystem output for generated artifacts."""

from __future__ import annotations

import json
import logging
from pathlib import Path
import re
import shutil
import tempfile

from ..observability import log_phase
from .artifact import GeneratedArtifactSet


_OWNERSHIP_DIRECTORY = ".artifact-ownership"
_ARTIFACT_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_LOGGER = logging.getLogger(__name__)


class ArtifactWriter:
    """Publish one generator's complete output set.

    Each set owns exactly the paths recorded in its artifact manifest. A later
    write for the same generator replaces that set and removes paths which the
    generator no longer emits. The shared output root itself is never cleared.
    """

    def write(
        self, artifacts: GeneratedArtifactSet, output_root: str | Path
    ) -> tuple[Path, ...]:
        with log_phase(
            _LOGGER,
            "artifact.write",
            artifact=artifacts.artifact_id,
            files=len(artifacts.artifacts),
        ):
            return self._write(artifacts, output_root)

    def _write(
        self, artifacts: GeneratedArtifactSet, output_root: str | Path
    ) -> tuple[Path, ...]:
        root = self._safe_output_root(output_root)
        paths = tuple(artifact.relative_path for artifact in artifacts.artifacts)
        self._validate_paths(paths)

        artifact_id = artifacts.artifact_id
        if _ARTIFACT_ID.fullmatch(artifact_id) is None:
            raise ValueError(f"invalid generated artifact id: {artifact_id!r}")

        with tempfile.TemporaryDirectory(
            prefix=f"bedrock-{artifact_id}-stage-"
        ) as directory:
            stage = Path(directory)
            for artifact in artifacts.artifacts:
                destination = stage / artifact.relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                if isinstance(artifact.content, bytes):
                    destination.write_bytes(artifact.content)
                else:
                    destination.write_text(artifact.content, encoding="utf-8")
            self._validate_stage(artifacts, stage)

            root.mkdir(parents=True, exist_ok=True)
            manifests = self._load_manifests(root)
            previous = manifests.pop(artifact_id, frozenset())
            manifest = self._manifest_path(root, artifact_id)
            self._validate_ownership(paths, previous, manifests)
            self._validate_existing_paths(root, paths, previous)

            written: list[Path] = []
            for relative_path in paths:
                destination = self._destination(root, relative_path)
                destination.parent.mkdir(parents=True, exist_ok=True)
                staged = stage / relative_path
                if not self._same_content(staged, destination):
                    shutil.copyfile(staged, destination)
                written.append(destination)

            for stale in sorted(previous - frozenset(paths), reverse=True):
                destination = self._destination(root, stale)
                if destination.exists():
                    if not destination.is_file() and not destination.is_symlink():
                        raise ValueError(
                            f"owned generated artifact is not a file: {destination}"
                        )
                    destination.unlink()
                    self._remove_empty_parents(destination.parent, root)

            manifest.parent.mkdir(parents=True, exist_ok=True)
            manifest.write_text(
                json.dumps(
                    {
                        "artifact_id": artifact_id,
                        "paths": [path.as_posix() for path in paths],
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )

        return tuple(written)

    @staticmethod
    def _same_content(staged: Path, destination: Path) -> bool:
        if not destination.is_file():
            return False
        if staged.stat().st_size != destination.stat().st_size:
            return False
        with staged.open("rb") as candidate, destination.open("rb") as current:
            while candidate_chunk := candidate.read(1024 * 1024):
                if candidate_chunk != current.read(len(candidate_chunk)):
                    return False
            return current.read(1) == b""

    @staticmethod
    def _safe_output_root(output_root: str | Path) -> Path:
        raw = Path(output_root).expanduser()
        if raw.is_symlink():
            raise ValueError(f"refusing symlinked output root: {raw}")
        root = raw.resolve()
        cwd = Path.cwd().resolve()
        unsafe = {Path("/").resolve(), Path.home().resolve(), cwd}
        if root in unsafe or cwd.is_relative_to(root):
            raise ValueError(f"refusing unsafe generated artifact output root: {root}")
        if root.exists() and not root.is_dir():
            raise ValueError(f"generated artifact output root is not a directory: {root}")
        return root

    @staticmethod
    def _validate_paths(paths: tuple[Path, ...]) -> None:
        path_set: set[Path] = set()
        for path in paths:
            if not path.parts or path == Path("."):
                raise ValueError("generated artifact path must name a file")
            if path.is_absolute() or ".." in path.parts:
                raise ValueError(f"generated artifact path escapes output root: {path}")
            if path.parts[0] == _OWNERSHIP_DIRECTORY:
                raise ValueError(
                    f"generated artifact path uses reserved ownership directory: {path}"
                )
            if path in path_set:
                raise ValueError(
                    "generated artifact paths overlap as file and directory: "
                    f"{path}, {path}"
                )
            path_set.add(path)
        for path in paths:
            for parent in path.parents:
                if parent == Path("."):
                    break
                if parent in path_set:
                    raise ValueError(
                        "generated artifact paths overlap as file and directory: "
                        f"{parent}, {path}"
                    )

    @staticmethod
    def _validate_stage(artifacts: GeneratedArtifactSet, stage: Path) -> None:
        for artifact in artifacts.artifacts:
            staged = stage / artifact.relative_path
            if not staged.is_file():
                raise RuntimeError(f"generated artifact was not staged: {artifact.relative_path}")
            actual = staged.read_bytes()
            expected = (
                artifact.content
                if isinstance(artifact.content, bytes)
                else artifact.content.encode("utf-8")
            )
            if actual != expected:
                raise RuntimeError(f"staged artifact differs: {artifact.relative_path}")

    @staticmethod
    def _manifest_path(root: Path, artifact_id: str) -> Path:
        return root / _OWNERSHIP_DIRECTORY / f"{artifact_id}.json"

    def _load_manifests(self, root: Path) -> dict[str, frozenset[Path]]:
        directory = root / _OWNERSHIP_DIRECTORY
        if not directory.exists():
            return {}
        if not directory.is_dir() or directory.is_symlink():
            raise ValueError(f"invalid artifact ownership directory: {directory}")
        manifests: dict[str, frozenset[Path]] = {}
        for source in sorted(directory.glob("*.json")):
            try:
                raw = json.loads(source.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                raise ValueError(f"invalid artifact ownership manifest: {source}") from error
            artifact_id = raw.get("artifact_id") if isinstance(raw, dict) else None
            raw_paths = raw.get("paths") if isinstance(raw, dict) else None
            if (
                not isinstance(artifact_id, str)
                or _ARTIFACT_ID.fullmatch(artifact_id) is None
                or source != self._manifest_path(root, artifact_id)
                or not isinstance(raw_paths, list)
                or not all(isinstance(item, str) for item in raw_paths)
            ):
                raise ValueError(f"invalid artifact ownership manifest: {source}")
            paths = tuple(Path(item) for item in raw_paths)
            try:
                self._validate_paths(paths)
            except ValueError as error:
                raise ValueError(f"invalid artifact ownership manifest: {source}") from error
            if len(paths) != len(set(paths)):
                raise ValueError(f"invalid artifact ownership manifest: {source}")
            manifests[artifact_id] = frozenset(paths)
        return manifests

    @staticmethod
    def _validate_ownership(
        paths: tuple[Path, ...],
        previous: frozenset[Path],
        other_manifests: dict[str, frozenset[Path]],
    ) -> None:
        claimed = frozenset(paths) | previous
        for other_id, other_paths in other_manifests.items():
            for path in claimed:
                for other in other_paths:
                    if (
                        path == other
                        or path.is_relative_to(other)
                        or other.is_relative_to(path)
                    ):
                        raise ValueError(
                            f"generated artifact path {path} conflicts with "
                            f"owner {other_id!r} path {other}"
                        )

    @staticmethod
    def _validate_existing_paths(
        root: Path,
        paths: tuple[Path, ...],
        previous: frozenset[Path],
    ) -> None:
        """Reject filesystem shapes which cannot be replaced as owned files.

        This check runs for the complete new and stale path sets before the
        writer mutates the output tree. In particular, it prevents a nested
        symlink from redirecting an otherwise valid relative output path.
        """

        new_paths = frozenset(paths)
        for relative_path in new_paths | previous:
            current = root
            for index, part in enumerate(relative_path.parts):
                current /= part
                if current.is_symlink():
                    raise ValueError(
                        "generated artifact path traverses a symlink: "
                        f"{relative_path}"
                    )
                if not current.exists():
                    continue
                if index < len(relative_path.parts) - 1 and not current.is_dir():
                    raise ValueError(
                        "generated artifact parent is not a directory: "
                        f"{current}"
                    )

            destination = root / relative_path
            if (
                relative_path in new_paths
                and relative_path not in previous
                and destination.exists()
            ):
                raise ValueError(
                    "refusing to replace unowned generated artifact path: "
                    f"{destination}"
                )
            if destination.exists() and not destination.is_file():
                action = "replace" if relative_path in new_paths else "remove"
                raise ValueError(
                    f"cannot {action} owned generated artifact as a file: "
                    f"{destination}"
                )

    @staticmethod
    def _destination(root: Path, relative_path: Path) -> Path:
        return root / relative_path

    @staticmethod
    def _remove_empty_parents(directory: Path, root: Path) -> None:
        current = directory
        while current != root and current.is_relative_to(root):
            try:
                current.rmdir()
            except OSError:
                return
            current = current.parent
