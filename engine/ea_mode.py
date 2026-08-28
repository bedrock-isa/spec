"""Representation and validation of one effective-address mode YAML file."""

from __future__ import annotations

import ast
from collections.abc import Iterator, Mapping, MutableMapping
from copy import deepcopy
from pathlib import Path
import re
from typing import Any

import yaml
from jsonschema import Draft202012Validator

try:
    from .encoding_metasyntax import EncodingMetasyntax
    from .reference import Reference, ReferenceError
    from .type_system import FieldType, FieldTypeKind, TypeSystem
except ImportError:  # Support loading engine directly on PYTHONPATH.
    from encoding_metasyntax import EncodingMetasyntax
    from reference import Reference, ReferenceError
    from type_system import FieldType, FieldTypeKind, TypeSystem


class EAMode(MutableMapping[str, Any]):
    """Encapsulate and validate one compact or extended ``mode.yaml``."""

    def __init__(
        self,
        data: Mapping[str, Any],
        source: str | Path,
        isa_root: str | Path | None = None,
        type_system: TypeSystem | None = None,
    ) -> None:
        self._data = deepcopy(dict(data))
        self.source = Path(source)
        self.isa_root = (
            Path(isa_root) if isa_root is not None else self._find_isa_root()
        )
        self.type_system = type_system or TypeSystem.load(self.isa_root)
        self.reference = self._reference_from_source()
        self.validate()

    @classmethod
    def load(
        cls,
        path: str | Path,
        isa_root: str | Path | None = None,
        type_system: TypeSystem | None = None,
    ) -> "EAMode":
        """Load and validate a mode YAML file."""

        source = Path(path)
        with source.open("r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
        if not isinstance(data, Mapping):
            raise ValueError(f"{source}: expected a YAML mapping")
        return cls(data, source, isa_root, type_system)

    def validate(self) -> None:
        """Validate this file without performing catalog-wide checks."""

        self._validate_mode_type_membership()
        raw_encodings = self._data.get("encodings")
        first_encoding = (
            raw_encodings[0]
            if isinstance(raw_encodings, list) and raw_encodings
            else None
        )
        first_pattern = (
            first_encoding.get("pattern")
            if isinstance(first_encoding, Mapping)
            else None
        )
        compact = isinstance(first_pattern, str)
        schema_name = "ea-mode-compact.yaml" if compact else "ea-mode-extended.yaml"
        schema = self._load_mapping(self.isa_root / "schemas" / schema_name)
        errors = sorted(
            Draft202012Validator(schema).iter_errors(self._data),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
        if errors:
            error = errors[0]
            location = ".".join(str(part) for part in error.absolute_path)
            where = f" at {location}" if location else ""
            raise ValueError(f"{self.source}{where}: {error.message}")

        if self.reference.element != self._data["id"]:
            raise ValueError(
                f"{self.source}: mode id {self._data['id']!r} does not match "
                f"reference element {self.reference.element!r}"
            )

        field_types = self.type_system.field_types
        payload_types = self.type_system.payload_types
        variants = [
            (
                EncodingMetasyntax.parse(encoding["pattern"]),
                encoding.get("payloads", []),
                encoding.get("autoupdate"),
                index,
            )
            for index, encoding in enumerate(self._data["encodings"])
        ]
        patterns = [pattern for pattern, _, _, _ in variants]
        if len(patterns) != len(set(patterns)):
            raise ValueError(f"{self.source}: encoding patterns must be unique")

        if compact:
            profile_type, profile_definition = self._profile_field_type(field_types)
            expected = profile_definition.bits
            for pattern in patterns:
                if pattern.bit_width != expected:
                    raise ValueError(
                        f"{self.source}: compact pattern has {pattern.bit_width} bits; "
                        f"{profile_type} requires {expected}"
                    )

        fields = self._data.get("fields", {})
        for pattern, _, _, index in variants:
            if set(fields) != pattern.fields:
                variant = f" encoding {index}" if index is not None else ""
                raise ValueError(
                    f"{self.source}:{variant} fields {sorted(fields)} do not match "
                    f"pattern characters {sorted(pattern.fields)}"
                )

        field_roles: list[str] = []
        for character, field in fields.items():
            field_type = field["type"]
            try:
                field_definition = field_types.resolve(field_type)
            except ReferenceError as error:
                raise ValueError(
                    f"{self.source}: unknown field type {field_type!r}"
                ) from error
            expected = field_definition.bits
            for pattern, _, _, index in variants:
                actual = pattern.field_width(character)
                if actual != expected:
                    variant = f" encoding {index}" if index is not None else ""
                    raise ValueError(
                        f"{self.source}:{variant} field {character!r} occupies "
                        f"{actual} bits; {field_type} requires {expected}"
                    )
            field_roles.append(field["role"])
        if len(field_roles) != len(set(field_roles)):
            raise ValueError(f"{self.source}: field roles must be unique")

        payload_roles: list[str] = []
        for _, payloads, _, index in variants:
            variant_roles: list[str] = []
            for payload in payloads:
                payload_type = payload["type"]
                try:
                    payload_types.resolve(payload_type)
                except ReferenceError as error:
                    raise ValueError(
                        f"{self.source}: unknown payload type {payload_type!r}"
                    ) from error
                role = payload["role"]
                variant_roles.append(role)
                if role not in payload_roles:
                    payload_roles.append(role)
            if len(variant_roles) != len(set(variant_roles)):
                variant = f" encoding {index}" if index is not None else ""
                raise ValueError(
                    f"{self.source}:{variant} payload roles must be unique"
                )

        segment = self._data.get("segment")
        if (
            segment
            and segment["source"] == "field"
            and segment["role"] not in field_roles
        ):
            raise ValueError(f"{self.source}: segment role has no matching field")
        for _, _, autoupdate, index in variants:
            if autoupdate and autoupdate["target"] not in field_roles:
                raise ValueError(
                    f"{self.source}: encoding {index} autoupdate target has no matching field"
                )
        self._validate_pseudocode(field_roles, payload_roles, compact)

    def save(self, path: str | Path | None = None) -> None:
        """Validate and write the mode to ``path`` or back to its source."""

        self.validate()
        destination = Path(path) if path is not None else self.source
        destination_reference = self._reference_from_source(destination)
        if destination_reference.element != self._data["id"]:
            raise ValueError(
                f"{destination}: mode id {self._data['id']!r} does not match "
                f"reference element {destination_reference.element!r}"
            )
        with destination.open("w", encoding="utf-8") as stream:
            yaml.safe_dump(
                self._data,
                stream,
                sort_keys=False,
                allow_unicode=True,
                default_flow_style=False,
            )
        self.source = destination
        self.reference = destination_reference

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
            if (parent / "schemas").is_dir() and (
                parent / "field_types.yaml"
            ).is_file():
                return parent
        raise ValueError(f"{self.source}: cannot locate ISA root")

    def _reference_from_source(self, path: str | Path | None = None) -> Reference:
        source_path = Path(path) if path is not None else self.source
        source = source_path.resolve()
        isa_root = self.isa_root.resolve()
        try:
            relative = source.relative_to(isa_root)
        except ValueError as error:
            raise ValueError(
                f"{source_path}: mode is outside ISA root {self.isa_root}"
            ) from error

        parts = relative.parts
        if len(parts) < 4 or parts[-1] != "mode.yaml":
            raise ValueError(
                f"{source_path}: expected a mode.yaml below a modes directory"
            )
        if parts[0] == "extensions":
            if len(parts) < 6:
                raise ValueError(f"{source_path}: incomplete extension mode path")
            owner = parts[1]
            logical_parts = list(parts[2:-1])
        else:
            owner = "base"
            logical_parts = list(parts[:-1])

        try:
            logical_parts.remove("modes")
        except ValueError as error:
            raise ValueError(f"{source_path}: expected a modes directory") from error
        if len(logical_parts) < 2:
            raise ValueError(f"{source_path}: mode reference has no logical path")
        try:
            return Reference(owner, tuple(logical_parts[:-1]), logical_parts[-1])
        except ReferenceError as error:
            raise ValueError(f"{source_path}: {error}") from error

    def _validate_mode_type_membership(self) -> None:
        mode_type = self.reference.path[-1]
        isa_root = self.isa_root.resolve()
        for parent in self.source.resolve().parents:
            if parent == isa_root.parent:
                break
            catalog = parent / "mode_types.yaml"
            if not catalog.is_file():
                continue
            mode_types = self._load_mapping(catalog).get("mode_types")
            if not isinstance(mode_types, list) or not all(
                isinstance(name, str) for name in mode_types
            ):
                raise ValueError(f"{catalog}: mode_types must be a list of names")
            if mode_type not in mode_types:
                raise ValueError(f"{catalog}: unlisted mode type {mode_type!r}")
            return
        raise ValueError(f"{self.source}: cannot locate mode_types.yaml")

    def _profile_field_type(
        self, field_types: Mapping[Reference, FieldType]
    ) -> tuple[Reference, FieldType]:
        profile = self.reference.path[0]
        candidates = [
            (reference, definition)
            for reference, definition in field_types.items()
            if definition.kind == FieldTypeKind.EFFECTIVE_ADDRESS
            and definition.profile == profile
        ]
        if len(candidates) != 1:
            raise ValueError(
                f"{self.source}: expected one effective-address field type for "
                f"profile {profile!r}; found {len(candidates)}"
            )
        return candidates[0]

    def _validate_pseudocode(
        self, field_roles: list[str], payload_roles: list[str], compact: bool
    ) -> None:
        kind = self._data["kind"]
        if kind == "extension":
            return

        text = self._data["pseudocode"]

        try:
            tree = ast.parse(text, mode="exec")
        except SyntaxError as error:
            raise ValueError(f"{self.source}: invalid pseudocode expression") from error
        if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Assign):
            raise ValueError(f"{self.source}: pseudocode must contain one assignment")
        assignment = tree.body[0]
        expected_result = "offset" if kind == "memory" else "value"
        if (
            len(assignment.targets) != 1
            or not isinstance(assignment.targets[0], ast.Name)
            or assignment.targets[0].id != expected_result
        ):
            raise ValueError(
                f"{self.source}: {kind} pseudocode must assign to {expected_result}"
            )

        allowed_lower = set(field_roles) | set(payload_roles) | {"scale"}
        if not compact:
            allowed_lower.add("displacement")
        allowed_nodes = (
            ast.Module,
            ast.Assign,
            ast.Name,
            ast.Load,
            ast.Store,
            ast.Constant,
            ast.BinOp,
            ast.UnaryOp,
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.USub,
        )
        for node in ast.walk(tree):
            if not isinstance(node, allowed_nodes):
                raise ValueError(
                    f"{self.source}: pseudocode does not allow {type(node).__name__}"
                )
            if isinstance(node, ast.Constant) and (
                not isinstance(node.value, int) or isinstance(node.value, bool)
            ):
                raise ValueError(f"{self.source}: pseudocode literals must be integers")
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                identifier = node.id
                if identifier not in allowed_lower and not re.fullmatch(
                    r"[A-Z][A-Z0-9_]*", identifier
                ):
                    raise ValueError(
                        f"{self.source}: unavailable pseudocode identifier {identifier!r}"
                    )

    @staticmethod
    def _load_mapping(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
        if not isinstance(data, dict):
            raise ValueError(f"{path}: expected a YAML mapping")
        return data

    @staticmethod
    def _positive_int(value: Any, name: str) -> int:
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError(f"{name} must be a positive integer")
        return value
