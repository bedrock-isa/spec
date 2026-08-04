"""Load per-instruction encoding forms as one global allocation space."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from defs_loader import load_extensions, load_field_types
from encoding_fields import FieldTypeRegistry, resolve_encoding_form
from defs_schema import (
    EncodingForm,
    EncodingsDocument,
    decode_encodings,
)
from encoding_architecture import ENCODING_CLASSES, EncodingClass

import yaml


@dataclass(frozen=True)
class LocatedEncoding:
    path: Path
    mnemonic: str
    form: EncodingForm


@dataclass(frozen=True)
class EncodingStore:
    defs_root: Path
    classes: tuple[EncodingClass, ...]
    encodings: tuple[LocatedEncoding, ...]
    field_types: FieldTypeRegistry

    @property
    def classes_by_name(self) -> dict[str, EncodingClass]:
        return {item.name: item for item in self.classes}

    def for_class(self, name: str) -> list[LocatedEncoding]:
        return [item for item in self.encodings if item.form.encoding_class == name]

    def for_mnemonic(self, mnemonic: str) -> list[LocatedEncoding]:
        return [item for item in self.encodings if item.mnemonic == mnemonic]


def _raw_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_encoding_store(defs_root: Path) -> EncodingStore:
    class_names = {item.name for item in ENCODING_CLASSES}
    extensions = load_extensions(defs_root)
    field_types = load_field_types(defs_root, extensions)
    encodings: list[LocatedEncoding] = []
    ids: dict[str, Path] = {}
    for path in sorted(defs_root.glob("**/instructions/*/encodings.yaml")):
        document = decode_encodings(path, _raw_yaml(path))
        if not isinstance(document, EncodingsDocument):  # pragma: no cover
            raise TypeError(document)
        mnemonic = path.parent.name
        for decoded_form in document.forms:
            form = resolve_encoding_form(decoded_form, field_types, path)
            if form.encoding_class not in class_names:
                raise ValueError(
                    f"{path}: form {form.id!r} references unknown class "
                    f"{form.encoding_class!r}"
                )
            previous = ids.get(form.id)
            if previous is not None:
                raise ValueError(
                    f"duplicate encoding id {form.id!r}: {previous} and {path}"
                )
            ids[form.id] = path
            encodings.append(LocatedEncoding(path, mnemonic, form))
    return EncodingStore(defs_root, ENCODING_CLASSES, tuple(encodings), field_types)


def encoding_form_dict(form: EncodingForm) -> dict:
    """Return the canonical serializable shape used by editor writes."""
    out: dict = {
        "id": form.id,
        "class": form.encoding_class,
        "bits": form.bits,
        "syntax": form.syntax,
    }
    if form.operands:
        operands = []
        for operand in form.operands:
            item = {
                "name": operand.name,
                "type": operand.type,
                "access": operand.access,
            }
            if operand.field is not None:
                item["field"] = operand.field
            if operand.domain is not None:
                item["domain"] = operand.domain
            if operand.ea_role is not None:
                item["ea_role"] = operand.ea_role
            if operand.ea_width is not None:
                item["ea_width"] = operand.ea_width
            operands.append(item)
        out["operands"] = operands
    has_size_selector = any(
        value.type.startswith("size.") for value in form.fields.values()
    )
    if form.sizes and not has_size_selector:
        out["sizes"] = list(form.sizes)
    if form.fields:
        out["fields"] = {
            name: {"type": value.type} for name, value in form.fields.items()
        }
    if form.constraints:
        constraints = []
        for constraint in form.constraints:
            item = {"field": constraint.field}
            if constraint.allow:
                item["allow"] = list(constraint.allow)
            if constraint.exclude is not None:
                item["exclude"] = constraint.exclude
            if constraint.reason is not None:
                item["reason"] = constraint.reason
            constraints.append(item)
        out["constraints"] = constraints
    if form.destination_overlap:
        out["destination_overlap"] = [
            {
                "operands": list(relation.operands),
                "rule": relation.rule,
            }
            for relation in form.destination_overlap
        ]
    if form.notes:
        out["notes"] = list(form.notes)
    return out


def allocation_entry_dict(
    located: LocatedEncoding,
    field_types: FieldTypeRegistry,
) -> dict:
    """Adapt a new encoding form to the claim/report algorithms."""
    form = located.form
    fields: dict[str, dict[str, object]] = {}

    def field_dict(type_name: str) -> dict[str, object]:
        spec = field_types.types[type_name]
        result: dict[str, object] = {
            "type": type_name,
            "kind": spec.allocation_kind,
            "width": spec.width,
        }
        if spec.size_codes:
            result["size_choices"] = list(spec.size_codes)
        return result

    for operand in form.operands:
        if operand.field is not None:
            fields[operand.field] = field_dict(operand.type)
    for name, value in form.fields.items():
        fields[name] = field_dict(value.type)
    out = {
        "id": form.id,
        "bits": form.bits,
        "text": form.syntax,
        "syntax": form.syntax,
        "fields": fields,
        "constraints": [
            item
            for item in encoding_form_dict(form).get("constraints", [])
        ],
        "source_path": str(located.path),
        "mnemonic": located.mnemonic,
    }
    if form.notes:
        out["notes"] = list(form.notes)
    if form.destination_overlap:
        out["destination_overlap"] = [
            {
                "operands": list(relation.operands),
                "rule": relation.rule,
            }
            for relation in form.destination_overlap
        ]
    return out


def class_entries(store: EncodingStore, name: str) -> list[dict]:
    return [
        allocation_entry_dict(item, store.field_types)
        for item in store.for_class(name)
    ]


def iter_entries(store: EncodingStore) -> Iterable[tuple[EncodingClass, LocatedEncoding, dict]]:
    classes = store.classes_by_name
    for located in store.encodings:
        yield (
            classes[located.form.encoding_class],
            located,
            allocation_entry_dict(located, store.field_types),
        )
