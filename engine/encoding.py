"""Typed representation and local loading of instruction encodings."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .encoding_metasyntax import EncodingMetasyntax
from .instruction_metasyntax import InstructionMetasyntax
from .reference import Reference
from .type_system import FieldType, PayloadType, TypeSystem
from .yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader


ConstraintValue = int | str


@dataclass(frozen=True, slots=True)
class FieldBinding:
    """One primary-encoding field marker and its logical representation."""

    marker: str
    role: str
    type: Reference[FieldType]
    access: str | None = None


@dataclass(frozen=True, slots=True)
class PayloadBinding:
    """One appended payload in encoded byte order."""

    role: str
    type: Reference[PayloadType]
    access: str | None = None


@dataclass(frozen=True, slots=True)
class OperandConstraint:
    """An allowed or excluded subset of one field role's value domain."""

    role: str
    reason: str
    allow: tuple[ConstraintValue, ...] = ()
    exclude: tuple[ConstraintValue, ...] = ()


@dataclass(frozen=True, slots=True)
class OperandOverlap:
    """The architectural aliasing relation between two encoded operands."""

    operands: tuple[str, str]
    type: str


@dataclass(frozen=True, slots=True)
class EncodingForm:
    """One locally named instruction encoding form."""

    id: str
    pattern: EncodingMetasyntax
    syntax: InstructionMetasyntax
    fields: tuple[FieldBinding, ...] = ()
    payloads: tuple[PayloadBinding, ...] = ()
    constraints: tuple[OperandConstraint, ...] = ()
    overlaps: tuple[OperandOverlap, ...] = ()

    def field_for_marker(self, marker: str) -> FieldBinding | None:
        return next((field for field in self.fields if field.marker == marker), None)

    def field_for_role(self, role: str) -> FieldBinding | None:
        return next((field for field in self.fields if field.role == role), None)


@dataclass(frozen=True, slots=True)
class EncodingCatalog:
    """The schema-decoded ``encodings.yaml`` for one instruction."""

    source: Path
    forms: tuple[EncodingForm, ...]

    @classmethod
    def load(
        cls,
        path: str | Path,
        types: TypeSystem,
        isa_root: str | Path | None = None,
    ) -> "EncodingCatalog":
        source = Path(path).resolve()
        root = (
            Path(isa_root).resolve()
            if isa_root is not None
            else cls._find_isa_root(source)
        )
        document = SchemaValidatedYamlLoader().load(
            source, root / "schemas/instruction-encodings.yaml"
        )

        forms: list[EncodingForm] = []
        for encoding_id, raw_form in document["encodings"].items():
            fields = tuple(
                cls._field(marker, representation, types)
                for marker, representation in raw_form.get("fields", {}).items()
            )
            payloads = tuple(
                cls._payload(representation, types)
                for representation in raw_form.get("payloads", ())
            )
            constraints = tuple(
                OperandConstraint(
                    role=constraint["role"],
                    reason=constraint["reason"],
                    allow=tuple(constraint.get("allow", ())),
                    exclude=tuple(constraint.get("exclude", ())),
                )
                for constraint in raw_form.get("constraints", ())
            )
            overlaps = tuple(
                OperandOverlap(tuple(overlap["operands"]), overlap["type"])
                for overlap in raw_form.get("overlaps", ())
            )
            forms.append(
                EncodingForm(
                    id=encoding_id,
                    pattern=EncodingMetasyntax.parse(raw_form["pattern"]),
                    syntax=InstructionMetasyntax.parse(raw_form["syntax"]),
                    fields=fields,
                    payloads=payloads,
                    constraints=constraints,
                    overlaps=overlaps,
                )
            )
        return cls(source=source, forms=tuple(forms))

    @staticmethod
    def _field(marker: str, raw: Mapping[str, Any], types: TypeSystem) -> FieldBinding:
        reference = Reference.parse(raw["type"])
        types.field_types.resolve(reference)
        return FieldBinding(marker, raw["role"], reference, raw.get("access"))

    @staticmethod
    def _payload(raw: Mapping[str, Any], types: TypeSystem) -> PayloadBinding:
        reference = Reference.parse(raw["type"])
        types.payload_types.resolve(reference)
        return PayloadBinding(raw["role"], reference, raw.get("access"))

    @staticmethod
    def _find_isa_root(source: Path) -> Path:
        for parent in source.parents:
            if (parent / "schemas/instruction-encodings.yaml").is_file():
                return parent
        raise ValueError(f"{source}: cannot locate ISA root")

    @staticmethod
    def _load_mapping(path: Path) -> dict[str, Any]:
        return YamlDocumentLoader().mapping(path)
