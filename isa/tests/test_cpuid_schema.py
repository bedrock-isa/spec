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

    def test_leaf_rejects_out_of_range_allocations_and_path_shaped_ids(self) -> None:
        document = {
            "id": "BAD/LEAF",
            "name": "Bad Leaf",
            "value": 65536,
            "queries": [
                {
                    "id": "QUERY",
                    "index": 0,
                    "fields": [{"id": "FIELD", "lsb": 64, "bits": 1}],
                }
            ],
        }

        self.assertGreaterEqual(len(list(self.leaf_validator.iter_errors(document))), 3)


if __name__ == "__main__":
    unittest.main()
