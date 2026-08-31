import tempfile
import unittest
from pathlib import Path

import yaml

from engine.reference import Reference, UnknownReferenceError
from engine.type_system import FieldTypeKind, PayloadTypeKind, TypeSystem


class TypeSystemTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self._write("extensions/extensions.yaml", {"extensions": ["SAMPLE"]})
        self._write(
            "field_types.yaml",
            {
                "field_types": {
                    "WIDTH": {
                        "type": "size_selector",
                        "bits": 1,
                        "values": [
                            {"value": 0, "code": "NARROW"},
                            {"value": 1, "code": "WIDE"},
                        ],
                    }
                }
            },
        )
        self._write(
            "payload_types.yaml",
            {
                "payload_types": {
                    "BASE_ONLY": {
                        "type": "immediate",
                        "bytes": 2,
                        "value_type": "unsigned_integer",
                    }
                }
            },
        )
        self._write(
            "extensions/SAMPLE/field_types.yaml",
            {
                "field_types": {
                    "COUNT": {
                        "type": "immediate",
                        "bits": 3,
                        "value_type": "unsigned_integer",
                    }
                }
            },
        )
        self._write("extensions/SAMPLE/payload_types.yaml", {"payload_types": {}})

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _write(self, relative: str, document: object) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")

    def test_loads_declared_owner_namespaces(self) -> None:
        types = TypeSystem.load(self.root)

        self.assertEqual(set(types.extensions), {"SAMPLE"})
        self.assertEqual(types.namespace("base").owner, "base")
        self.assertEqual(types.namespace("SAMPLE").owner, "SAMPLE")

    def test_projects_typed_definitions_into_global_indexes(self) -> None:
        types = TypeSystem.load(self.root)
        width = types.field_types[Reference.parse("base.field_types.WIDTH")]
        count = types.field_types[Reference.parse("SAMPLE.field_types.COUNT")]
        payload = types.payload_types[Reference.parse("base.payload_types.BASE_ONLY")]

        self.assertIs(width, types.base.field_types[width.reference])
        self.assertIs(count, types.extensions["SAMPLE"].field_types[count.reference])
        self.assertIs(payload, types.base.payload_types[payload.reference])
        self.assertIs(width.kind, FieldTypeKind.SIZE_SELECTOR)
        self.assertEqual(
            tuple(value.code for value in width.values), ("NARROW", "WIDE")
        )
        self.assertIs(payload.kind, PayloadTypeKind.IMMEDIATE)

    def test_reference_resolution_does_not_fall_back_across_owners(self) -> None:
        types = TypeSystem.load(self.root)

        with self.assertRaises(UnknownReferenceError):
            types.payload_types.resolve(
                Reference.parse("SAMPLE.payload_types.BASE_ONLY")
            )

    def test_ignores_an_undeclared_extension_namespace(self) -> None:
        self._write(
            "extensions/UNLISTED/field_types.yaml",
            {
                "field_types": {
                    "Hidden": {
                        "type": "immediate",
                        "bits": 1,
                        "value_type": "unsigned_integer",
                    }
                }
            },
        )
        self._write("extensions/UNLISTED/payload_types.yaml", {"payload_types": {}})

        types = TypeSystem.load(self.root)

        self.assertEqual(set(types.extensions), {"SAMPLE"})
        with self.assertRaises(UnknownReferenceError):
            types.field_types.resolve(Reference.parse("UNLISTED.field_types.Hidden"))


if __name__ == "__main__":
    unittest.main()
