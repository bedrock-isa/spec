import tempfile
import unittest
from pathlib import Path

import yaml

from engine.encoding import EncodingCatalog
from engine.reference import UnknownReferenceError
from engine.type_system import TypeSystem


class EncodingCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]
        cls.types = TypeSystem.load(cls.isa_root)

    def test_loads_typed_add_forms_in_source_order(self) -> None:
        catalog = EncodingCatalog.load(
            self.isa_root / "instructions/definitions/ADD/encodings.yaml",
            self.types,
            self.isa_root,
        )

        self.assertEqual(catalog.forms[0].id, "q_8_sp")
        register_form = catalog.forms[1]
        self.assertEqual(register_form.syntax.mnemonic, "ADD")
        self.assertEqual(register_form.pattern.bit_width, 14)
        self.assertEqual(
            str(register_form.field_for_marker("s").type),
            "base.field_types.Rn",
        )

    def test_resolves_payload_types_while_loading(self) -> None:
        catalog = EncodingCatalog.load(
            self.isa_root / "instructions/definitions/JMP/encodings.yaml",
            self.types,
            self.isa_root,
        )
        payload_types = {
            str(payload.type) for form in catalog.forms for payload in form.payloads
        }
        self.assertIn("base.payload_types.DISP16S", payload_types)

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
