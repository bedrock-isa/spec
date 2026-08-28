import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


class InstructionMetasyntaxSchemaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        isa_root = Path(__file__).parents[1]
        cls.schema = yaml.safe_load(
            (isa_root / "schemas/instruction-metasyntax.yaml").read_text(
                encoding="utf-8"
            )
        )

    def test_is_a_valid_string_schema(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        self.assertEqual(self.schema["type"], "string")
        self.assertEqual(self.schema["minLength"], 1)


if __name__ == "__main__":
    unittest.main()
