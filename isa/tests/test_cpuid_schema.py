import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


class CpuidSchemaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        schemas = Path(__file__).parents[1] / "schemas"
        cls.class_validator = Draft202012Validator(
            yaml.safe_load((schemas / "cpuid-class.yaml").read_text(encoding="utf-8"))
        )
        cls.leaf_validator = Draft202012Validator(
            yaml.safe_load((schemas / "cpuid-leaf.yaml").read_text(encoding="utf-8"))
        )

    def test_class_requires_exactly_one_allocation_source(self) -> None:
        definition = {"id": "BASE", "name": "Base", "value": 0}
        overlay = {
            "id": "EXTENSIONS",
            "name": "Extensions",
            "extends": "base.cpuid.EXTENSIONS",
        }

        self.assertEqual(list(self.class_validator.iter_errors(definition)), [])
        self.assertEqual(list(self.class_validator.iter_errors(overlay)), [])
        self.assertNotEqual(
            list(self.class_validator.iter_errors({**definition, **overlay})), []
        )

    def test_leaf_accepts_fixed_and_strided_query_indexes(self) -> None:
        document = {
            "id": "SAVE_AREA_LAYOUT",
            "name": "Save Area Layout",
            "value": 4,
            "queries": [
                {
                    "id": "SIZE",
                    "index": 1,
                    "fields": [{"id": "BYTES", "lsb": 0, "bits": 64}],
                },
                {
                    "id": "DESCRIPTOR_A",
                    "index": {"first": 3, "last": 65535, "stride": 2},
                },
            ],
        }

        self.assertEqual(list(self.leaf_validator.iter_errors(document)), [])

    @staticmethod
    def leaf_document() -> dict:
        return {
            "id": "LEAF",
            "name": "Bad Leaf",
            "value": 1,
            "queries": [
                {
                    "id": "QUERY",
                    "index": 0,
                    "fields": [{"id": "FIELD", "lsb": 0, "bits": 1}],
                }
            ],
        }

    def assert_leaf_rejected_at(self, document: dict, path: tuple[object, ...]) -> None:
        errors = list(self.leaf_validator.iter_errors(document))
        self.assertTrue(errors)
        self.assertIn(path, {tuple(error.absolute_path) for error in errors})

    def test_leaf_rejects_path_shaped_id(self) -> None:
        document = self.leaf_document()
        document["id"] = "BAD/LEAF"
        self.assert_leaf_rejected_at(document, ("id",))

    def test_leaf_rejects_out_of_range_leaf_value(self) -> None:
        document = self.leaf_document()
        document["value"] = 65536
        self.assert_leaf_rejected_at(document, ("value",))

    def test_leaf_rejects_field_outside_result_width(self) -> None:
        document = self.leaf_document()
        document["queries"][0]["fields"][0]["lsb"] = 64
        self.assert_leaf_rejected_at(document, ("queries", 0, "fields", 0, "lsb"))


if __name__ == "__main__":
    unittest.main()
