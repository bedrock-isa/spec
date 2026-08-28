import tempfile
import unittest
from pathlib import Path

import yaml

from engine.reference import UnknownReferenceError
from engine.type_system import FieldType, FieldTypeKind, PayloadType, TypeSystem


class TypeSystemTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.types = TypeSystem.load(Path(__file__).parents[1])

    def test_indexes_base_and_extension_field_types(self) -> None:
        self.assertEqual(self.types.field_types["base.field_types.Rn"].bits, 4)
        self.assertEqual(self.types.field_types["FP.field_types.Fn"].bits, 4)
        self.assertEqual(self.types.field_types["VECTOR.field_types.Vn"].bits, 5)

    def test_indexes_size_selector_field_types(self) -> None:
        self.assertEqual(self.types.field_types["base.field_types.SIZE_BWLQ"].bits, 2)
        self.assertEqual(self.types.field_types["FP.field_types.SIZE_SD"].bits, 1)
        self.assertEqual(
            self.types.field_types["VECTOR.field_types.SIZE_VTYPE"].bits, 3
        )

    def test_indexes_base_and_extension_payload_types(self) -> None:
        self.assertEqual(self.types.payload_types["base.payload_types.DISP8S"].bytes, 1)
        self.assertEqual(self.types.payload_types["FP.payload_types.IMMDF"].bytes, 8)

    def test_exposes_concrete_type_objects_without_a_common_parent(self) -> None:
        field = self.types.field_types["base.field_types.SIZE_BWLQ"]
        payload = self.types.payload_types["base.payload_types.IMM16"]

        self.assertIsInstance(field, FieldType)
        self.assertIsInstance(payload, PayloadType)
        self.assertEqual(field.kind, FieldTypeKind.SIZE_SELECTOR)
        self.assertEqual([value.code for value in field.values], ["B", "W", "L", "Q"])
        self.assertFalse(isinstance(field, PayloadType))

    def test_groups_types_by_owner_namespace(self) -> None:
        vector = self.types.namespace("VECTOR")

        self.assertIs(
            vector.field_types["VECTOR.field_types.Vn"],
            self.types.field_types["VECTOR.field_types.Vn"],
        )
        self.assertEqual(len(vector.payload_types), 0)

    def test_missing_type_is_not_resolved_by_scope(self) -> None:
        with self.assertRaises(UnknownReferenceError):
            self.types.payload_types.resolve("VECTOR.payload_types.DISP8S")

    def test_does_not_load_types_from_an_undeclared_extension(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "extensions/UNLISTED").mkdir(parents=True)
            (root / "field_types.yaml").write_text(
                yaml.safe_dump({"field_types": {}}), encoding="utf-8"
            )
            (root / "payload_types.yaml").write_text(
                yaml.safe_dump({"payload_types": {}}), encoding="utf-8"
            )
            (root / "extensions/extensions.yaml").write_text(
                yaml.safe_dump({"extensions": []}), encoding="utf-8"
            )
            (root / "extensions/UNLISTED/field_types.yaml").write_text(
                yaml.safe_dump(
                    {
                        "field_types": {
                            "Hidden": {
                                "type": "immediate",
                                "bits": 1,
                                "value_type": "unsigned_integer",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            types = TypeSystem.load(root)

        with self.assertRaises(UnknownReferenceError):
            types.field_types.resolve("UNLISTED.field_types.Hidden")


if __name__ == "__main__":
    unittest.main()
