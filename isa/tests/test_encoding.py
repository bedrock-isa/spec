import tempfile
import unittest
from pathlib import Path

import yaml

from engine.encoding import EncodingCatalog
from engine.reference import Reference, UnknownReferenceError
from engine.type_system import TypeSystem


class EncodingCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]
        cls.types = TypeSystem.load(cls.isa_root)

    def test_loads_typed_forms_in_declared_source_order(self) -> None:
        document = {
            "encodings": {
                "q_8_sp": {"pattern": "0001110", "syntax": "ADD.Q 8, SP"},
                "q_4_sp": {"pattern": "0001111", "syntax": "ADD.Q 4, SP"},
            }
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "encodings.yaml"
            path.write_text(
                yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
            )
            catalog = EncodingCatalog.load(path, self.types, self.isa_root)

        self.assertEqual(tuple(form.id for form in catalog.forms), tuple(document["encodings"]))

    def test_resolves_payload_types_while_loading(self) -> None:
        catalog = EncodingCatalog.load(
            self.isa_root / "instructions/definitions/JMP/encodings.yaml",
            self.types,
            self.isa_root,
        )
        payload_types = {
            payload.type for form in catalog.forms for payload in form.payloads
        }
        self.assertIn(Reference.parse("base.payload_types.DISP16S"), payload_types)

    def test_rejects_unknown_type_reference(self) -> None:
        document = {
            "encodings": {
                "rn_s": {
                    "pattern": "000000ssssdddd",
                    "syntax": "ADD Rn(s)",
                    "fields": {
                        "s": {"role": "src", "type": "base.field_types.MISSING"},
                        "d": {"role": "dst", "type": "base.field_types.Rn"},
                    },
                }
            }
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "encodings.yaml"
            path.write_text(yaml.safe_dump(document), encoding="utf-8")
            with self.assertRaises(UnknownReferenceError):
                EncodingCatalog.load(path, self.types, self.isa_root)


if __name__ == "__main__":
    unittest.main()
