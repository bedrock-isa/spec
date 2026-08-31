"""Representation and validation of one instruction YAML file."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, MutableMapping
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


class MnemonicDirectoryMismatchError(ValueError):
    """The instruction mnemonic disagrees with its owning directory."""


class UnknownRepeatObservedValueError(ValueError):
    """A repeat contract names neither an operand nor the computed result."""


class Instruction(MutableMapping[str, Any]):
    """Encapsulate and internally validate one ``instruction.yaml``."""

    def __init__(
        self,
        data: Mapping[str, Any],
        source: str | Path,
        isa_root: str | Path | None = None,
    ) -> None:
        self._data = deepcopy(dict(data))
        self.source = Path(source)
        self.isa_root = Path(isa_root) if isa_root is not None else self._find_isa_root()
        self.validate()

    @classmethod
    def load(
        cls, path: str | Path, isa_root: str | Path | None = None
    ) -> "Instruction":
        """Load and validate one instruction YAML file."""

        source = Path(path)
        with source.open("r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
        if not isinstance(data, Mapping):
            raise ValueError(f"{source}: expected a YAML mapping")
        return cls(data, source, isa_root)

    def validate(self) -> None:
        """Validate this file without inspecting its encoding catalog."""

        self._validate_source(self.source)
        schema = self._load_mapping(self.isa_root / "schemas/instruction.yaml")
        errors = sorted(
            Draft202012Validator(schema).iter_errors(self._data),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
        if errors:
            error = errors[0]
            location = ".".join(str(part) for part in error.absolute_path)
            where = f" at {location}" if location else ""
            raise ValueError(f"{self.source}{where}: {error.message}")

        mnemonic = self._data["mnemonic"]
        if self.source.parent.name != mnemonic:
            raise MnemonicDirectoryMismatchError(
                f"{self.source}: mnemonic {mnemonic!r} does not match "
                f"instruction directory {self.source.parent.name!r}"
            )

        repeat = self._data.get("repeat")
        if repeat and repeat["type"] == "repcc":
            observed = repeat["observed_value"]
            if observed != "computed" and observed not in self._data["operands"]:
                raise UnknownRepeatObservedValueError(
                    f"{self.source}: repeat observed_value {observed!r} does not "
                    "name an operand"
                )

    def save(self, path: str | Path | None = None) -> None:
        """Validate and write to ``path`` or back to the original source."""

        destination = Path(path) if path is not None else self.source
        previous_source = self.source
        self.source = destination
        try:
            self.validate()
            with destination.open("w", encoding="utf-8") as stream:
                yaml.safe_dump(
                    self._data,
                    stream,
                    sort_keys=False,
                    allow_unicode=True,
                    default_flow_style=False,
                )
        except Exception:
            self.source = previous_source
            raise

    def to_dict(self) -> dict[str, Any]:
        return deepcopy(self._data)

    def __getattr__(self, name: str) -> Any:
        data = self.__dict__.get("_data", {})
        if name in data:
            return deepcopy(data[name])
        raise AttributeError(name)

    def __getitem__(self, key: str) -> Any:
        return deepcopy(self._data[key])

    def __setitem__(self, key: str, value: Any) -> None:
        previous = deepcopy(self._data)
        self._data[key] = deepcopy(value)
        try:
            self.validate()
        except Exception:
            self._data = previous
            raise

    def __delitem__(self, key: str) -> None:
        previous = deepcopy(self._data)
        del self._data[key]
        try:
            self.validate()
        except Exception:
            self._data = previous
            raise

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def _find_isa_root(self) -> Path:
        for parent in (self.source.parent, *self.source.parents):
            if (parent / "schemas/instruction.yaml").is_file():
                return parent
        raise ValueError(f"{self.source}: cannot locate ISA root")

    @staticmethod
    def _validate_source(source: Path) -> None:
        if source.name != "instruction.yaml":
            raise ValueError(f"{source}: expected a file named instruction.yaml")

    @staticmethod
    def _load_mapping(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
        if not isinstance(data, Mapping):
            raise ValueError(f"{path}: expected a YAML mapping")
        return dict(data)
