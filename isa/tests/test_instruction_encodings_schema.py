import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from engine.encoding_metasyntax import EncodingMetasyntax
from engine.instruction_metasyntax import InstructionMetasyntax
from engine.type_system import TypeSystem


class InstructionEncodingsSchemaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        isa_root = Path(__file__).parents[1]
        cls.isa_root = isa_root
        cls.schema = yaml.safe_load(
            (isa_root / "schemas/instruction-encodings.yaml").read_text(
                encoding="utf-8"
            )
        )
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)
        cls.types = TypeSystem.load(isa_root)

    @staticmethod
    def document() -> dict:
        return {
            "encodings": {
                "l_q_z_rn_s_rn_d": {
                    "pattern": "00001zssssdddd",
                    "syntax": "ADD.{L|Q}(z) Rn(s), Rn(d)",
                    "fields": {
                        "z": {
                            "role": "size",
                            "type": "base.field_types.SIZE_LQ",
                        },
                        "s": {
                            "role": "src",
                            "type": "base.field_types.Rn",
                        },
                        "d": {
                            "role": "dst",
                            "type": "base.field_types.Rn",
                        },
                    },
                    "constraints": [
                        {
                            "role": "dst",
                            "exclude": ["immediate"],
                            "reason": "invalid_destination",
                        }
                    ],
                    "overlaps": [
                        {
                            "operands": ["src", "dst"],
                            "type": "same_value",
                        }
                    ],
                },
                "imm16s": {
                    "pattern": "111101000000000000",
                    "syntax": "JMP <imm16s>",
                    "payloads": [
                        {
                            "role": "target",
                            "type": "base.payload_types.DISP16S",
                        }
                    ],
                },
            }
        }

    def assert_valid(self, document: dict) -> None:
        self.assertEqual(list(self.validator.iter_errors(document)), [])

    def assert_invalid(self, document: dict) -> None:
        self.assertNotEqual(list(self.validator.iter_errors(document)), [])

    def test_accepts_local_id_mapping_and_split_representations(self) -> None:
        self.assert_valid(self.document())

    def test_all_concrete_encoding_files_validate(self) -> None:
        roots = (
            self.isa_root / "instructions/definitions",
            self.isa_root / "extensions/FP/instructions/definitions",
            self.isa_root / "extensions/VECTOR/instructions/definitions",
            self.isa_root / "extensions/FPTRANSA/instructions/definitions",
        )
        for root in roots:
            catalog = yaml.safe_load(
                (root / "instructions.yaml").read_text(encoding="utf-8")
            )["instructions"]
            actual = sorted(
                path.name
                for path in root.iterdir()
                if path.is_dir() and "<" not in path.name
            )
            self.assertEqual(sorted(catalog), actual)

            for mnemonic in catalog:
                path = root / mnemonic / "encodings.yaml"
                document = yaml.safe_load(path.read_text(encoding="utf-8"))
                with self.subTest(path=path):
                    self.assert_valid(document)

                for encoding_id, encoding in document["encodings"].items():
                    syntax = InstructionMetasyntax(encoding["syntax"])
                    pattern = EncodingMetasyntax(encoding["pattern"])
                    fields = encoding.get("fields", {})
                    with self.subTest(path=path, encoding=encoding_id):
                        self.assertEqual(syntax.mnemonic, mnemonic)
                        self.assertEqual(syntax.encoding_id, encoding_id)
                        self.assertEqual(pattern.fields, set(fields))
                        for marker, field in fields.items():
                            definition = self.types.field_types.resolve(field["type"])
                            self.assertEqual(
                                pattern.field_width(marker), definition.bits
                            )
                        for payload in encoding.get("payloads", []):
                            self.types.payload_types.resolve(payload["type"])

                        for companion in ("descriptions.tex", "semantics.sail"):
                            self.assertTrue((path.parent / companion).is_file())
    def test_rejects_noncanonical_redundant_form_properties(self) -> None:
        encoding_id = "l_q_z_rn_s_rn_d"
        for property_name, value in (
            ("class", "short"),
            ("bits", "00001zssssdddd"),
            ("operands", []),
            ("sizes", ["L", "Q"]),
            ("destination_overlap", []),
        ):
            document = self.document()
            document["encodings"][encoding_id][property_name] = value
            with self.subTest(property=property_name):
                self.assert_invalid(document)

    def test_rejects_nonlocal_ids_and_unknown_pattern_widths(self) -> None:
        document = self.document()
        encoding_id = "l_q_z_rn_s_rn_d"
        document["encodings"]["short.add.rn_rn"] = document["encodings"].pop(
            encoding_id
        )
        self.assert_invalid(document)

        document = self.document()
        document["encodings"][encoding_id]["pattern"] = "00000000"
        self.assert_invalid(document)

    def test_constraint_selects_exactly_one_operation(self) -> None:
        document = self.document()
        encoding_id = "l_q_z_rn_s_rn_d"
        constraint = document["encodings"][encoding_id]["constraints"][0]
        constraint["allow"] = [0]
        self.assert_invalid(document)

        document = self.document()
        del document["encodings"][encoding_id]["constraints"][0]["exclude"]
        self.assert_invalid(document)


if __name__ == "__main__":
    unittest.main()
