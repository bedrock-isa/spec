"""Load per-instruction encoding forms as one global allocation space."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from collections import Counter

from defs_schema import (
    EncodingClass,
    EncodingClassesDocument,
    EncodingForm,
    EncodingsDocument,
    decode_encoding_classes,
    decode_encodings,
)

import yaml


@dataclass(frozen=True)
class LocatedEncoding:
    path: Path
    mnemonic: str
    form: EncodingForm


@dataclass(frozen=True)
class EncodingStore:
    defs_root: Path
    class_path: Path
    classes: tuple[EncodingClass, ...]
    encodings: tuple[LocatedEncoding, ...]

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
    class_path = defs_root / "encoding_classes.yaml"
    class_doc = decode_encoding_classes(class_path, _raw_yaml(class_path))
    if not isinstance(class_doc, EncodingClassesDocument):  # pragma: no cover
        raise TypeError(class_doc)
    class_names = {item.name for item in class_doc.classes}
    encodings: list[LocatedEncoding] = []
    ids: dict[str, Path] = {}
    for path in sorted(defs_root.glob("**/instructions/*/encodings.yaml")):
        document = decode_encodings(path, _raw_yaml(path))
        if not isinstance(document, EncodingsDocument):  # pragma: no cover
            raise TypeError(document)
        mnemonic = path.parent.name
        for form in document.forms:
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
    return EncodingStore(defs_root, class_path, class_doc.classes, tuple(encodings))


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
            operands.append(item)
        out["operands"] = operands
    if form.sizes:
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
    if form.notes:
        out["notes"] = list(form.notes)
    return out


def allocation_entry_dict(located: LocatedEncoding) -> dict:
    """Adapt a new encoding form to the claim/report algorithms."""
    form = located.form
    widths = Counter(char for char in form.bits if char not in "01?")
    kind_by_type = {
        "size": "size",
        "Rn": "rn",
        "Fn": "freg",
        "EA": "ea7",
        "condition": "condition",
    }
    immediate_types = {
        "flags_bitmap",
        "pair_id",
        "fp_pair_id",
        "pt_level",
        "fconst_id",
    }

    def field_kind(field_type: str) -> str:
        if field_type.startswith("imm") or field_type in immediate_types:
            return "immediate"
        return kind_by_type.get(field_type, "bits")

    fields: dict[str, dict[str, object]] = {}
    for operand in form.operands:
        if operand.field is not None:
            fields[operand.field] = {
                "type": operand.type,
                "kind": field_kind(operand.type),
                "width": widths[operand.field],
            }
    for name, value in form.fields.items():
        fields[name] = {
            "type": value.type,
            "kind": field_kind(value.type),
            "width": widths[name],
        }
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
    return out


def class_entries(store: EncodingStore, name: str) -> list[dict]:
    return [allocation_entry_dict(item) for item in store.for_class(name)]


def iter_entries(store: EncodingStore) -> Iterable[tuple[EncodingClass, LocatedEncoding, dict]]:
    classes = store.classes_by_name
    for located in store.encodings:
        yield classes[located.form.encoding_class], located, allocation_entry_dict(located)
