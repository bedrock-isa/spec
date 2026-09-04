"""Representation and validation of one effective-address mode YAML file."""

from __future__ import annotations

import ast
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass, replace
from pathlib import Path
import re
from enum import StrEnum
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from .entity import Entity
from .encoding_metasyntax import EncodingMetasyntax
from .reference import Reference, ReferenceError
from .type_system import EffectiveAddressFieldType, FieldType, PayloadType, TypeSystem


class EAModeSchemaError(ValueError):
    """An EA mode document violates its structural schema."""


class EABaseSource(StrEnum):
    """Typed source of the base term in one EA mode expression."""

    NONE = "none"
    ENCODED = "encoded"
    STACK_POINTER = "SP"
    PROGRAM_COUNTER = "PC"
    ZERO = "zero"


def _load_name_list(path: Path, key: str) -> tuple[str, ...]:
    with path.open("r", encoding="utf-8") as stream:
        raw = yaml.safe_load(stream)
    values = raw.get(key) if isinstance(raw, Mapping) else None
    if not isinstance(values, list) or any(not isinstance(item, str) for item in values):
        raise ValueError(f"{path}: expected a {key} list of names")
    if len(set(values)) != len(values):
        raise ValueError(f"{path}: {key} must not contain duplicates")
    return tuple(values)


@dataclass(frozen=True, slots=True)
class EAModeCatalog:
    """One explicitly named EA mode catalog in the architectural namespace."""

    source: Path
    owner: str
    profile: str
    mode_type: str
    name: str
    modes: tuple[str, ...]

    @classmethod
    def load(
        cls,
        source: str | Path,
        *,
        owner: str,
        profile: str,
        mode_type: str,
    ) -> "EAModeCatalog":
        path = Path(source)
        with path.open("r", encoding="utf-8") as stream:
            raw = yaml.safe_load(stream)
        if not isinstance(raw, Mapping) or set(raw) != {"name", "modes"}:
            raise ValueError(f"{path}: expected exactly name and modes")
        name = raw["name"]
        modes = raw["modes"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{path}: name must be a non-empty string")
        if not isinstance(modes, list) or any(
            not isinstance(item, str)
            or re.fullmatch(r"[a-z][a-z0-9_]*", item) is None
            for item in modes
        ):
            raise ValueError(f"{path}: modes must be a list of names")
        if len(set(modes)) != len(modes):
            raise ValueError(f"{path}: modes must not contain duplicates")
        try:
            Reference(owner, (profile, "modes"), mode_type)
            for mode_id in modes:
                Reference(owner, (profile, "modes", mode_type), mode_id)
        except ReferenceError as error:
            raise ValueError(f"{path}: invalid EA catalog identity: {error}") from error
        return cls(path, owner, profile, mode_type, name.strip(), tuple(modes))

    @classmethod
    def discover(
        cls,
        isa_root: str | Path,
        type_system: TypeSystem,
        owners: tuple[str, ...] | None = None,
    ) -> tuple["EAModeCatalog", ...]:
        root = Path(isa_root).resolve()
        profiles: dict[str, str] = {}
        for definition in type_system.field_types.values():
            if not isinstance(definition, EffectiveAddressFieldType):
                continue
            if definition.owner in profiles:
                raise ValueError(
                    f"{root}: owner {definition.owner!r} has multiple EA profiles"
                )
            profiles[definition.owner] = definition.profile
        owner_order = owners or tuple(profiles)
        catalogs: list[EAModeCatalog] = []
        for owner in owner_order:
            profile = profiles.get(owner)
            if profile is None:
                continue
            profile_root = (
                root / profile
                if owner == "base"
                else root / "extensions" / owner / profile
            )
            modes_root = profile_root / "modes"
            mode_types = _load_name_list(modes_root / "mode_types.yaml", "mode_types")
            for mode_type in mode_types:
                catalogs.append(
                    cls.load(
                        modes_root / mode_type / "modes.yaml",
                        owner=owner,
                        profile=profile,
                        mode_type=mode_type,
                    )
                )
        return tuple(catalogs)

    @classmethod
    def containing(
        cls,
        mode_path: str | Path,
        isa_root: str | Path,
        type_system: TypeSystem,
    ) -> "EAModeCatalog":
        source = Path(mode_path).resolve()
        matches = [
            catalog
            for catalog in cls.discover(isa_root, type_system)
            if source
            in {
                (catalog.source.parent / mode_id / "mode.yaml").resolve()
                for mode_id in catalog.modes
            }
        ]
        if len(matches) != 1:
            raise ValueError(
                f"{mode_path}: expected exactly one declaring EA catalog, found "
                f"{len(matches)}"
            )
        return matches[0]

    def reference(self, mode_id: str) -> Reference["EAMode"]:
        if mode_id not in self.modes:
            raise ValueError(f"{self.source}: undeclared EA mode {mode_id!r}")
        return Reference(self.owner, (self.profile, "modes", self.mode_type), mode_id)

    def mode_path(self, mode_id: str) -> Path:
        self.reference(mode_id)
        return self.source.parent / mode_id / "mode.yaml"


@dataclass(frozen=True, slots=True)
class EAField:
    """One encoded field used by every encoding of an EA mode."""

    symbol: str
    role: str
    type: Reference[FieldType]


@dataclass(frozen=True, slots=True)
class EAPayload:
    """One payload consumed after an EA selector or descriptor."""

    role: str
    type: Reference[PayloadType]


@dataclass(frozen=True, slots=True)
class EAAutoupdate:
    """One architected register update attached to an EA encoding."""

    target: str
    update_type: str
    difference: int | str


@dataclass(frozen=True, slots=True)
class EAEncoding:
    """One normalized wire encoding of an EA mode."""

    patterns: tuple[str, ...]
    payloads: tuple[EAPayload, ...]
    autoupdate: EAAutoupdate | None


@dataclass(frozen=True, slots=True)
class FixedEASegment:
    register: str


@dataclass(frozen=True, slots=True)
class FieldEASegment:
    role: str


EASegment = FixedEASegment | FieldEASegment


@dataclass(frozen=True, slots=True)
class EAExtension:
    id: str
    bytes: int


@dataclass(frozen=True, slots=True)
class EAMode(Entity):
    """Common immutable identity and encodings of an effective-address mode."""

    reference: Reference["EAMode"]
    source: Path
    isa_root: Path
    type_system: TypeSystem
    catalog: EAModeCatalog
    id: str
    name: str
    encodings: tuple[EAEncoding, ...]
    fields: tuple[EAField, ...]

    @classmethod
    def load(
        cls,
        path: str | Path,
        isa_root: str | Path | None = None,
        type_system: TypeSystem | None = None,
        *,
        catalog: EAModeCatalog | None = None,
    ) -> "EAMode":
        source = Path(path)
        with source.open("r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
        if not isinstance(data, Mapping):
            raise ValueError(f"{source}: expected a YAML mapping")
        return _EAModeSource(
            data, source, isa_root, type_system, catalog=catalog
        ).decode()

    def field(self, symbol: str) -> EAField:
        return next(field for field in self.fields if field.symbol == symbol)

    def field_for_role(self, role: str) -> EAField | None:
        return next((field for field in self.fields if field.role == role), None)

    def field_type_reference(self, symbol: str) -> Reference[FieldType]:
        return self.field(symbol).type

    def payload_type_reference(
        self, encoding_index: int, payload_index: int
    ) -> Reference[PayloadType]:
        return self.encodings[encoding_index].payloads[payload_index].type

    def with_encoding(self, encoding: EAEncoding) -> "EAMode":
        update = encoding.autoupdate
        variant = update.update_type if update is not None else "plain"
        return replace(self, encodings=(encoding,), name=f"{self.name} / {variant}")


@dataclass(frozen=True, slots=True)
class ImmediateEAMode(EAMode):
    syntax: str
    pseudocode: str


@dataclass(frozen=True, slots=True)
class MemoryEAMode(EAMode):
    syntax: str
    pseudocode: str
    segment: EASegment | None
    base_source: EABaseSource


@dataclass(frozen=True, slots=True)
class CompactExtensionEAMode(EAMode):
    extension: EAExtension


@dataclass(frozen=True, slots=True)
class ExtendedExtensionEAMode(EAMode):
    syntax: str
    extension: EAExtension


class _EAModeSource:
    """Validate and decode one authored compact or extended ``mode.yaml``."""

    def __init__(
        self,
        data: Mapping[str, Any],
        source: str | Path,
        isa_root: str | Path | None = None,
        type_system: TypeSystem | None = None,
        *,
        catalog: EAModeCatalog | None = None,
    ) -> None:
        self._data = deepcopy(dict(data))
        self.source = Path(source)
        self.isa_root = (
            Path(isa_root) if isa_root is not None else self._find_isa_root()
        )
        self.type_system = type_system or TypeSystem.load(self.isa_root)
        self.catalog = catalog or EAModeCatalog.containing(
            self.source, self.isa_root, self.type_system
        )
        self.mode_id = self.source.parent.name
        self.reference: Reference[EAMode] = self.catalog.reference(self.mode_id)
        self._field_type_references: dict[str, Reference[FieldType]] = {}
        self._payload_type_references: dict[tuple[int, int], Reference[PayloadType]] = {}
        self.validate()

    def validate(self) -> None:
        """Validate this file without performing catalog-wide checks."""

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
            raise EAModeSchemaError(f"{self.source}{where}: {error.message}")

        field_type_references, payload_type_references = self._parse_type_references()

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
                field_definition = field_types.resolve(field_type_references[character])
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
            for payload_index, payload in enumerate(payloads):
                payload_type = payload["type"]
                try:
                    payload_types.resolve(payload_type_references[index, payload_index])
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
        self._field_type_references = field_type_references
        self._payload_type_references = payload_type_references

    @property
    def base_source(self) -> EABaseSource:
        """Return the structurally parsed base term used by this mode."""

        if self._data["kind"] != "memory":
            return EABaseSource.NONE
        tree = ast.parse(self._data["pseudocode"], mode="exec")
        assignment = tree.body[0]
        assert isinstance(assignment, ast.Assign)
        expression = assignment.value
        names = {
            node.id
            for node in ast.walk(expression)
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
        }
        field_roles = {
            field["role"] for field in self._data.get("fields", {}).values()
        }
        candidates = []
        if "base" in field_roles and "base" in names:
            candidates.append(EABaseSource.ENCODED)
        if "SP" in names:
            candidates.append(EABaseSource.STACK_POINTER)
        if "PC" in names:
            candidates.append(EABaseSource.PROGRAM_COUNTER)
        if any(
            isinstance(node, ast.Constant)
            and isinstance(node.value, int)
            and not isinstance(node.value, bool)
            and node.value == 0
            for node in ast.walk(expression)
        ):
            candidates.append(EABaseSource.ZERO)
        if not candidates:
            return EABaseSource.NONE
        if len(candidates) != 1:
            raise ValueError(
                f"{self.source}: memory pseudocode identifies multiple base sources"
            )
        return candidates[0]

    def decode(self) -> EAMode:
        fields = tuple(
            EAField(symbol, raw["role"], self._field_type_references[symbol])
            for symbol, raw in self._data.get("fields", {}).items()
        )
        encodings = tuple(
            EAEncoding(
                (raw["pattern"],)
                if isinstance(raw["pattern"], str)
                else tuple(raw["pattern"]),
                tuple(
                    EAPayload(
                        payload["role"],
                        self._payload_type_references[encoding_index, payload_index],
                    )
                    for payload_index, payload in enumerate(raw.get("payloads", ()))
                ),
                EAAutoupdate(
                    raw["autoupdate"]["target"],
                    raw["autoupdate"]["type"],
                    raw["autoupdate"]["difference"],
                )
                if "autoupdate" in raw
                else None,
            )
            for encoding_index, raw in enumerate(self._data["encodings"])
        )
        common = (
            self.reference,
            self.source,
            self.isa_root,
            self.type_system,
            self.catalog,
            self.mode_id,
            self._data["name"],
            encodings,
            fields,
        )
        kind = self._data["kind"]
        if kind == "immediate":
            return ImmediateEAMode(
                *common, self._data["syntax"], self._data["pseudocode"]
            )
        if kind == "memory":
            raw_segment = self._data.get("segment")
            segment: EASegment | None
            if raw_segment is None:
                segment = None
            elif raw_segment["source"] == "fixed":
                segment = FixedEASegment(raw_segment["register"])
            else:
                segment = FieldEASegment(raw_segment["role"])
            return MemoryEAMode(
                *common,
                self._data["syntax"],
                self._data["pseudocode"],
                segment,
                self.base_source,
            )
        extension = EAExtension(
            self._data["extension"]["id"], self._data["extension"]["bytes"]
        )
        if self.catalog.mode_type == "compact":
            return CompactExtensionEAMode(*common, extension)
        return ExtendedExtensionEAMode(*common, self._data["syntax"], extension)

    def _find_isa_root(self) -> Path:
        for parent in (self.source.parent, *self.source.parents):
            if (parent / "schemas").is_dir() and (
                parent / "field_types.yaml"
            ).is_file():
                return parent
        raise ValueError(f"{self.source}: cannot locate ISA root")

    def _profile_field_type(
        self, field_types: Mapping[Reference[FieldType], FieldType]
    ) -> tuple[Reference[FieldType], FieldType]:
        profile = self.catalog.profile
        candidates = [
            (reference, definition)
            for reference, definition in field_types.items()
            if isinstance(definition, EffectiveAddressFieldType)
            and definition.profile == profile
        ]
        if len(candidates) != 1:
            raise ValueError(
                f"{self.source}: expected one effective-address field type for "
                f"profile {profile!r}; found {len(candidates)}"
            )
        return candidates[0]

    def _parse_type_references(
        self,
    ) -> tuple[
        dict[str, Reference[FieldType]],
        dict[tuple[int, int], Reference[PayloadType]],
    ]:
        field_references: dict[str, Reference[FieldType]] = {}
        for symbol, field in self._data.get("fields", {}).items():
            try:
                field_references[symbol] = Reference.parse(field["type"])
            except ReferenceError as error:
                raise ValueError(
                    f"{self.source}: invalid field type {field['type']!r}"
                ) from error

        payload_references: dict[tuple[int, int], Reference[PayloadType]] = {}
        for encoding_index, encoding in enumerate(self._data["encodings"]):
            for payload_index, payload in enumerate(encoding.get("payloads", ())):
                try:
                    payload_references[encoding_index, payload_index] = Reference.parse(
                        payload["type"]
                    )
                except ReferenceError as error:
                    raise ValueError(
                        f"{self.source}: invalid payload type {payload['type']!r}"
                    ) from error
        return field_references, payload_references

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
