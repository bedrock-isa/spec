"""Shared typed loading and schema validation for YAML authoring sources."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


class YamlDocumentLoader:
    """Decode YAML while enforcing the mapping root used by ISA registries."""

    def mapping(self, path: str | Path) -> dict[str, Any]:
        source = Path(path)
        with source.open("r", encoding="utf-8") as stream:
            document = yaml.safe_load(stream)
        if not isinstance(document, Mapping):
            raise ValueError(f"{source}: expected a YAML mapping")
        return dict(document)


class SchemaValidatedYamlLoader:
    """Load mapping documents and report a stable first schema diagnostic."""

    def __init__(self, documents: YamlDocumentLoader | None = None) -> None:
        self.documents = documents or YamlDocumentLoader()

    def load(
        self,
        source: str | Path,
        schema: str | Path | Mapping[str, object],
    ) -> dict[str, Any]:
        source_path = Path(source)
        document = self.documents.mapping(source_path)
        schema_document = (
            self.documents.mapping(schema)
            if isinstance(schema, (str, Path))
            else dict(schema)
        )
        errors = sorted(
            Draft202012Validator(schema_document).iter_errors(document),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
        if errors:
            error = errors[0]
            location = ".".join(str(part) for part in error.absolute_path)
            where = f" at {location}" if location else ""
            raise ValueError(f"{source_path}{where}: {error.message}")
        return document
