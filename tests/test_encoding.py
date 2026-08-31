import unittest
from pathlib import Path

from engine.encoding import EncodingCatalog
from engine.reference import UnknownReferenceError
from engine.type_system import TypeSystem


class EncodingCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1] / "isa"
        cls.types = TypeSystem.load(cls.isa_root)

    def test_rejects_unknown_type_reference(self) -> None:
        import tempfile
        import yaml

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
